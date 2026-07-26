import re
from collections import defaultdict

import httpx
from langchain.tools import tool

from app.core.config import settings


def _normalize(text: str) -> str:
    """去掉常见符号、空格、全角半角差异等，用于宽松比较。"""
    if not text:
        return ""
    return re.sub(r"[\s\*\_\-—–\.。,，、:：;；\"'`「『」』()（）\[\]【】]+", "", text)


def _parse_area_tokens_from_keyword(keyword: str):
    """
    从用户输入的 keyword 里提取出可能的省/市/区县名。
    返回 dict(province, city, district, stripped_keyword)。
    """
    text = keyword or ""
    result = {"province": "", "city": "", "district": "", "stripped": text}

    district_re = re.compile(
        r"([\u4e00-\u9fa5]{2,}(?:自治县|自治州|特别行政区|地区|盟|旗|自治旗|林区|新区|区|县))"
    )
    city_re = re.compile(r"([\u4e00-\u9fa5]{2,}(?:市))")
    province_re = re.compile(r"([\u4e00-\u9fa5]{2,}(?:省|自治区|特别行政区))")

    hits = []  # (token, kind, span)

    for m in province_re.finditer(text):
        hits.append((m.group(1), "province", m.span()))
    for m in city_re.finditer(text):
        hits.append((m.group(1), "city", m.span()))
    for m in district_re.finditer(text):
        hits.append((m.group(1), "district", m.span()))

    # 按出现顺序去掉 tokens，得到 stripped keyword
    spans_to_remove = [span for _, _, span in hits]
    spans_to_remove.sort(key=lambda x: x[0])
    stripped_parts = []
    cursor = 0
    for s, e in spans_to_remove:
        if cursor < s:
            stripped_parts.append(text[cursor:s])
        cursor = max(cursor, e)
    if cursor < len(text):
        stripped_parts.append(text[cursor:])
    result["stripped"] = ("".join(stripped_parts)).strip(" ，,。.;；:：的位于在") or text

    for token, kind, _ in hits:
        if not result[kind]:
            result[kind] = token

    return result


@tool
async def location_tool(keyword: str) -> dict:
    """
    查询地点。

    返回：

    success=True
        唯一地点，可继续查询天气。

    need_clarify=True
        地点存在歧义，需要用户继续说明。
    """

    area_hint = _parse_area_tokens_from_keyword(keyword)

    url = f"{settings.AMAP_BASE_URL}/v5/place/text"

    try:

        async with httpx.AsyncClient(timeout=10) as client:

            response = await client.get(
                url,
                params={
                    "key": settings.AMAP_API_KEY,
                    "keywords": keyword,
                    "page_size": 10,
                    "page_num": 1,
                },
            )

            data = response.json()

    except Exception as e:

        return {
            "success": False,
            "message": f"高德地图请求失败：{str(e)}"
        }

    print("AMap 返回：", data)

    if data.get("status") != "1":

        return {
            "success": False,
            "message": data.get("info", "高德地图查询失败。")
        }

    pois = data.get("pois", [])

    if not pois:

        return {
            "success": False,
            "message": f"没有找到『{keyword}』。"
        }

    # =============================
    # 过滤：优先保留风景名胜、景点类 POI
    # 避免停车场、游客中心、检票口等附属设施在不同区县导致行政区歧义
    # =============================

    SCENIC_TYPECODES_PREFIX = (
        "110",
    )

    SCENIC_NAME_KEYWORDS = (
        "景区", "景点", "风景区", "旅游区", "旅游景区",
        "公园", "地质公园", "森林公园", "观景台", "观景点",
    )

    NOISE_NAME_KEYWORDS = (
        "停车场", "游客服务中心", "游客中心", "检票口",
        "入口", "出口", "大门", "西门", "北门", "东门", "南门",
        "厕所", "卫生间", "餐厅", "商店", "酒店", "民宿",
    )

    def _is_scenic(poi) -> bool:
        typecode = poi.get("typecode", "") or ""
        name = poi.get("name", "") or ""
        for kw in NOISE_NAME_KEYWORDS:
            if kw in name:
                return False
        if typecode.startswith(SCENIC_TYPECODES_PREFIX):
            return True
        for kw in SCENIC_NAME_KEYWORDS:
            if kw in name:
                return True
        return False

    scenic_pois = [p for p in pois if _is_scenic(p)]

    if scenic_pois:
        pois = scenic_pois

    # =============================
    # 硬逻辑1：如果用户在 keyword 里明确提到了某个省/市/区县，就只保留对应行政区的 POI
    # 例：「临泽县的张掖七彩丹霞景区」→ 只留 adname == 临泽县
    # =============================

    def _poi_area_matches(poi) -> bool:
        province_hit = (not area_hint["province"]) or _normalize(area_hint["province"]) == _normalize(poi.get("pname"))
        city_hit = (not area_hint["city"]) or _normalize(area_hint["city"]) == _normalize(poi.get("cityname"))
        district_hit = (not area_hint["district"]) or _normalize(area_hint["district"]) == _normalize(poi.get("adname"))
        return province_hit and city_hit and district_hit

    if area_hint["province"] or area_hint["city"] or area_hint["district"]:
        area_filtered = [p for p in pois if _poi_area_matches(p)]
        if area_filtered:
            pois = area_filtered
            print(f"[location_tool] 根据 keyword 内行政区限定筛选后剩 {len(pois)} 条："
                  f"省={area_hint['province']} 市={area_hint['city']} 区/县={area_hint['district']}")

    if not pois:
        return {
            "success": False,
            "message": f"没有找到符合行政区条件的『{keyword}』。"
        }

    # =============================
    # 按行政区分组
    # =============================

    area_map = defaultdict(list)

    for poi in pois:

        province = poi.get("pname", "")
        city = poi.get("cityname", "")
        district = poi.get("adname", "")

        area_key = (
            province,
            city,
            district,
        )

        area_map[area_key].append(poi)

    # =============================
    # 唯一行政区 → 直接返回
    # =============================

    if len(area_map) == 1:

        first = pois[0]

        longitude = ""
        latitude = ""

        location = first.get("location", "")

        if location:

            try:

                longitude, latitude = location.split(",")

            except ValueError:

                pass

        return {

            "success": True,

            "keyword": keyword,

            "name": first.get("name"),

            "province": first.get("pname"),

            "city": first.get("cityname"),

            "district": first.get("adname"),

            "address": first.get("address"),

            "longitude": longitude,

            "latitude": latitude,
        }

    # =============================
    # 硬逻辑2：多行政区 → 使用「主景点匹配度」策略
    # 如果某个行政区下的 POI 的 name 就是用户搜的核心景区名（或核心景区名是该 POI name 的精确主体），
    # 就认定它是主景点，直接 success，不再让用户澄清。
    #
    # 例：搜「张掖七彩丹霞景区」，返回两个行政区：
    #   临泽县:  name == 张掖七彩丹霞景区        -> 命中主景点
    #   肃南县:  name == 张掖七彩丹霞景区卧虎峡  -> 是子景点，不命中
    # 此时直接返回临泽县那条。
    # =============================

    core_targets = []
    raw = _normalize(keyword)
    stripped = _normalize(area_hint["stripped"])
    if stripped and stripped not in core_targets:
        core_targets.append(stripped)
    if raw and raw not in core_targets:
        core_targets.append(raw)

    # 再补一个宽松版本：去掉常见后缀如"景区/风景区"再比
    def _chop_suffixes(s: str) -> str:
        suffixes = (
            "风景区", "旅游景区", "旅游区", "景区", "景点",
            "地质公园", "森林公园", "湿地公园", "公园",
        )
        changed = True
        while changed:
            changed = False
            for suf in suffixes:
                if s.endswith(suf) and len(s) > len(suf):
                    s = s[: -len(suf)]
                    changed = True
        return s

    for t in list(core_targets):
        chopped = _chop_suffixes(t)
        if chopped and chopped != t and len(chopped) >= 2:
            core_targets.append(chopped)

    best_poi = None
    best_score = -1

    for poi in pois:
        name_norm = _normalize(poi.get("name", ""))
        if not name_norm:
            continue
        score = 0
        # 完全相等（最强命中）
        for t in core_targets:
            if name_norm == t:
                score = max(score, 1000)
        # POI name 去掉子景点后缀后等于核心名（张掖七彩丹霞景区卧虎峡 -> 去掉卧虎峡 -> 张掖七彩丹霞景区 == 目标）
        # 也考虑：目标是 POI name 的前缀
        for t in core_targets:
            if not t:
                continue
            if len(name_norm) == len(t):
                continue  # 已经算在完全相等里
            if name_norm.startswith(t):
                suffix_len = len(name_norm) - len(t)
                # 后缀越短，越接近主景点
                if suffix_len <= 8:
                    score = max(score, 500 - suffix_len * 10)
            if t.startswith(name_norm) and len(name_norm) >= 2:
                score = max(score, 200)

        if score > best_score:
            best_score = score
            best_poi = poi

    if best_poi is not None and best_score >= 200:
        # 有明显的"主景点"，就直接返回，不再让用户澄清
        longitude = ""
        latitude = ""
        location = best_poi.get("location", "")
        if location:
            try:
                longitude, latitude = location.split(",")
            except ValueError:
                pass
        print(
            f"[location_tool] 多行政区但命中主景点：score={best_score} "
            f"name={best_poi.get('name')} 区县={best_poi.get('adname')}，直接 success"
        )
        return {
            "success": True,
            "keyword": keyword,
            "name": best_poi.get("name"),
            "province": best_poi.get("pname"),
            "city": best_poi.get("cityname"),
            "district": best_poi.get("adname"),
            "address": best_poi.get("address"),
            "longitude": longitude,
            "latitude": latitude,
        }

    # =============================
    # 仍无法唯一确定 → 返回需要澄清
    # =============================

    options = []

    for (province, city, district), poi_list in area_map.items():

        first = poi_list[0]

        options.append({

            "name": first.get("name"),

            "province": province,

            "city": city,

            "district": district,

            "address": first.get("address"),

        })

    return {

        "need_clarify": True,

        "keyword": keyword,

        "message": f"找到多个『{keyword}』，需要用户进一步确认。",

        "options": options,
    }
