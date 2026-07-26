import json
import re

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)

from app.ai.executor import execute
from app.ai.model import llm
from app.ai.planner import plan
from app.ai.prompts import SYSTEM_PROMPT


# =============================
# 行政区识别工具（与 location_tool 保持一致）
# =============================

def _parse_area_tokens_from_text(text: str):
    """
    从任意文本（用户消息、AI 回复等）里识别出省/市/区县名。
    """
    result = {"province": "", "city": "", "district": ""}
    if not text:
        return result

    district_re = re.compile(
        r"([\u4e00-\u9fa5]{2,}(?:自治县|自治州|特别行政区|地区|盟|旗|自治旗|林区|新区|区|县))"
    )
    city_re = re.compile(r"([\u4e00-\u9fa5]{2,}(?:市))")
    province_re = re.compile(r"([\u4e00-\u9fa5]{2,}(?:省|自治区|特别行政区))")

    for m in province_re.finditer(text):
        if not result["province"]:
            result["province"] = m.group(1)
    for m in city_re.finditer(text):
        if not result["city"]:
            result["city"] = m.group(1)
    for m in district_re.finditer(text):
        if not result["district"]:
            result["district"] = m.group(1)
    return result


def _normalize_area(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"[\s\*\_\-—–\.。,，、:：;；\"'`「『」』()（）\[\]【】]+", "", text)


def _parse_selection_index(user_text: str):
    """
    解析用户回复中的选择序号。
    返回 0-based index，或 None 表示不是选择。
    """
    text = (user_text or "").strip()
    if not text:
        return None

    # 纯数字
    m = re.fullmatch(r"\s*([0-9一二三四五六七八九十])\s*[.、．:：]?\s*", text)
    if m:
        raw = m.group(1)
        digit_map = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
        try:
            n = int(raw)
        except ValueError:
            n = digit_map.get(raw, 0)
        if n >= 1:
            return n - 1

    # 第N个 / 选第N个
    m = re.search(r"第\s*([0-9一二三四五六七八九十])\s*[个项款条]?", text)
    if m:
        raw = m.group(1)
        digit_map = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
        try:
            n = int(raw)
        except ValueError:
            n = digit_map.get(raw, 0)
        if n >= 1:
            return n - 1

    return None


def _extract_options_from_ai_reply(ai_text: str):
    """
    从上一轮 AI 的回复中提取列举的地点选项。
    支持格式：
      1. **XXX（YYY）**：位于ZZZ
      2. "XXX"：位于ZZZ
      1. XXX（YYY）：...
    返回 list[dict(name, province, city, district)]
    """
    options = []
    lines = (ai_text or "").splitlines()
    item_re = re.compile(
        r"^\s*["
        r"0-9一二三四五六七八九十"
        r"]+\s*[.、．:：)\)]\s*"  # 序号 + 分隔符
        r"["
        r"\"'`「『\*"
        r"]*"  # 可选左引号
        r"(.+?)"  # 名称
        r"["
        r"\"'`」』\*"
        r"]*\s*"  # 可选右引号
        r"[：:]\s*(.*)"  # 描述
    )
    # 括号里的区县/城市
    paren_re = re.compile(r"[（(]([^（）()]*)[）)]")
    # 描述里的 "位于临泽县" / "位于张掖市临泽县"
    located_re = re.compile(r"位于[\s：:]*([^\s，,。；;]+)")

    for line in lines:
        m = item_re.match(line)
        if not m:
            continue
        raw_name = m.group(1).strip()
        desc = m.group(2).strip() if m.lastindex and m.lastindex >= 2 else ""

        # 去掉 name 本身前后的描述（括号）
        name_clean = raw_name
        paren_extras = []
        pm = paren_re.search(name_clean)
        while pm:
            paren_extras.append(pm.group(1))
            name_clean = (name_clean[: pm.start()] + name_clean[pm.end():]).strip()
            pm = paren_re.search(name_clean)

        province = city = district = ""

        # 1) 括号/描述里的 "位于XX县"
        full_context = " ".join(paren_extras + [desc])
        lm = located_re.search(full_context)
        if lm:
            location_hint = lm.group(1)
            # 可能是 张掖市临泽县 / 临泽县 / 肃南裕固族自治县
            dm = re.match(r"(.+?市)?(.+?(?:区|县|旗|自治县|市))$", location_hint)
            if dm:
                if dm.group(1):
                    city = dm.group(1).rstrip("市")
                district = dm.group(2)
            else:
                district = location_hint

        options.append({
            "name": name_clean,
            "province": province,
            "city": city,
            "district": district,
            "raw_text": raw_name,
        })

    return options


def _build_location_keyword_from_option(opt: dict) -> str:
    """
    根据提取出的选项构造「精确」的 location keyword。
    优先级：区县 > 城市 + 景区名 > 纯景区名。
    目的：确保 location_tool（内部的高德 + 天气 API）能唯一命中行政区。
    """
    # 注意：天气 API 的城市查询要传 区县 才精准。
    parts = []
    if opt.get("city"):
        parts.append(opt["city"])
    if opt.get("district"):
        parts.append(opt["district"])
    # 最后附上景区名（如果还不够的话）
    if opt.get("name"):
        parts.append(opt["name"])
    # 去重，保持顺序
    seen = set()
    ordered = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        key = re.sub(r"[省市县区旗自治县]+$", "", p)
        if key and key in seen:
            continue
        seen.add(key)
        ordered.append(p)
    if ordered:
        return "".join(ordered)
    return opt.get("name") or opt.get("raw_text") or ""


def _apply_selection_override(messages: list, plan_result: dict) -> dict:
    """
    兜底覆盖：
    (A) 用户在上一轮 AI 给出地点选项后回复了数字/「第N个」
        → 直接用解析出的确切区县+景区名覆盖 Planner 的模糊 keyword
    (B) 用户在消息中明确提到了省/市/区县名，但 Planner 给出的 location_tool keyword 里没有该行政区名
        → 把行政区名拼进 keyword，避免 location_tool 因缺少限定而返回 need_clarify
    两种兜底都保证：必须有 location+weather 工具。
    """
    # ==========================
    # 找到最近的 user 消息和上一条 ai 消息
    # ==========================
    last_user_text = ""
    last_ai_text = ""
    n = len(messages)
    for i in range(n - 1, -1, -1):
        m = messages[i]
        if isinstance(m, HumanMessage) and not last_user_text:
            last_user_text = m.content or ""
            continue
        if isinstance(m, AIMessage) and last_user_text and not last_ai_text:
            last_ai_text = m.content or ""
            break

    if not last_user_text:
        return plan_result

    # ==========================
    # 收集 Planner 当前的 tools
    # ==========================
    original_tools = plan_result.get("tools", []) or []

    # 定位当前 location_tool 的 keyword（如果有）
    current_location_keyword = ""
    for t in original_tools:
        if t.get("name") == "location_tool":
            current_location_keyword = (t.get("args") or {}).get("keyword", "") or ""
            break

    # ==========================
    # 情况 A：用户回复数字选上一轮的选项
    # ==========================
    idx = _parse_selection_index(last_user_text) if last_ai_text else None
    case_a_applied = False
    if idx is not None:
        options = _extract_options_from_ai_reply(last_ai_text)
        if options and idx < len(options):
            selected = options[idx]
            precise_keyword = _build_location_keyword_from_option(selected)
            if precise_keyword:
                current_location_keyword = precise_keyword
                case_a_applied = True
                print(
                    f"\n[Selection Override] 用户选择 #{idx + 1}，命中选项：{selected}，"
                    f"重写 location keyword -> {current_location_keyword}\n"
                )

    # ==========================
    # 情况 B：用户消息里直接写了省/市/区县名 → 把行政区名拼进 location keyword
    # 例：用户说「位于临泽县的张掖七彩丹霞景区」，但 Planner 只写了 keyword=张掖七彩丹霞景区
    #     -> 我们覆盖为「临泽县张掖七彩丹霞景区」，location_tool 会用行政区过滤掉肃南县的 POI
    # ==========================
    user_area = _parse_area_tokens_from_text(last_user_text)
    keyword_area = _parse_area_tokens_from_text(current_location_keyword)

    # 当用户消息里有 区县/市/省，但 Planner 的 keyword 里没有对应层级时，补上
    missing_prefix_parts = []
    def _area_contains(outer, inner) -> bool:
        return bool(outer) and (
            _normalize_area(outer) in _normalize_area(inner)
            or _normalize_area(inner) in _normalize_area(outer)
        )

    if user_area["province"] and not _area_contains(user_area["province"], keyword_area["province"]):
        missing_prefix_parts.append(user_area["province"])
    if user_area["city"] and not _area_contains(user_area["city"], keyword_area["city"]):
        missing_prefix_parts.append(user_area["city"])
    if user_area["district"] and not _area_contains(user_area["district"], keyword_area["district"]):
        missing_prefix_parts.append(user_area["district"])

    case_b_applied = False
    if missing_prefix_parts and current_location_keyword:
        # 去重后拼到 keyword 最前面
        seen = set()
        ordered = []
        for p in missing_prefix_parts + [current_location_keyword]:
            p = (p or "").strip()
            if not p:
                continue
            key = _normalize_area(p)
            if key in seen:
                continue
            seen.add(key)
            ordered.append(p)
        new_keyword = "".join(ordered)
        if new_keyword != current_location_keyword:
            print(
                f"\n[Area Override] 用户消息提到行政区 {user_area}，"
                f"Planner keyword 缺失 -> {current_location_keyword} => {new_keyword}\n"
            )
            current_location_keyword = new_keyword
            case_b_applied = True

    # ==========================
    # 如果 A 或 B 任一命中，就重写 plan_result
    # ==========================
    if not (case_a_applied or case_b_applied):
        return plan_result

    # 若没有 location/weather（比如 Planner 抽风输出 tools:[]），但我们有了 keyword，就补齐工具
    if not current_location_keyword:
        return plan_result

    new_tools = []
    for t in original_tools:
        name = t.get("name")
        if name in ("location_tool", "weather_tool"):
            continue
        new_tools.append(t)

    new_tools.append({
        "name": "location_tool",
        "args": {"keyword": current_location_keyword},
    })

    weather_exists = any(t.get("name") == "weather_tool" for t in new_tools)
    if not weather_exists:
        new_tools.append({
            "name": "weather_tool",
            "args": {},
        })

    return {"tools": new_tools}


async def chat_with_tools(messages):

    """
    Planner
        ↓
    Executor
        ↓
    Final LLM
    """

    # ==========================
    # 最近10条历史
    # ==========================

    history = messages[-10:]

    # ==========================
    # Planner（传入完整对话历史，让其理解用户回复「1」「第一个」等选择场景）
    # ==========================

    plan_result = await plan(history)

    print("\n==============================")
    print("Planner Result")
    print(json.dumps(plan_result, ensure_ascii=False, indent=2))
    print("==============================\n")

    # ==========================
    # 确定性兜底：用户回复「1」「第一个」等数字选择时，直接覆盖 Planner 的输入为精确区县名
    # 避免：location_tool(七彩丹霞景区) -> need_clarify -> 再选再查 still need_clarify 的死循环
    # ==========================

    plan_result = _apply_selection_override(history, plan_result)

    if plan_result.get("tools"):
        print("\n==============================")
        print("Plan (After Override)")
        print(json.dumps(plan_result, ensure_ascii=False, indent=2))
        print("==============================\n")

    # ==========================
    # Executor
    # ==========================

    tool_results = await execute(plan_result)

    print("\n==============================")
    print("Tool Results")
    print(json.dumps(tool_results, ensure_ascii=False, indent=2))
    print("==============================\n")

    # ==========================
    # 构造最终 Prompt
    # ==========================

    final_messages = [

        SystemMessage(
            content=SYSTEM_PROMPT,
        )

    ]

    final_messages.extend(history)

    if tool_results:

        final_messages.append(

            SystemMessage(

                content=(
                    "下面是工具返回的数据。\n"
                    "请根据工具结果回答用户。\n\n"
                    + json.dumps(
                        tool_results,
                        ensure_ascii=False,
                        indent=2,
                    )
                )

            )

        )

    # ==========================
    # Streaming
    # ==========================

    async for chunk in llm.astream(final_messages):

        if chunk.content:

            yield chunk.content
