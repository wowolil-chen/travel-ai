import requests
from collections import defaultdict

from langchain.tools import tool

from app.core.config import settings


@tool
def location_tool(keyword: str) -> dict:
    """
    查询地点。

    返回：

    success=True
        唯一地点，可继续查询天气。

    need_clarify=True
        地点存在歧义，需要用户继续说明。
    """

    url = f"{settings.AMAP_BASE_URL}/v5/place/text"

    response = requests.get(
        url,
        params={
            "key": settings.AMAP_API_KEY,
            "keywords": keyword,
            "page_size": 10,
            "page_num": 1,
        },
        timeout=10,
    )

    data = response.json()

    print("AMap 返回：", data)

    if data.get("status") != "1":

        return {
            "success": False,
            "message": "高德地图查询失败。"
        }

    pois = data.get("pois", [])

    if not pois:

        return {
            "success": False,
            "message": f"没有找到『{keyword}』。"
        }

    # =============================
    # 按 行政区 分组
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
    # 唯一行政区
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
    # 多个行政区
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