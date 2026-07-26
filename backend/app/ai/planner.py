import json

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    AIMessage,
    BaseMessage,
)

from app.ai.model import planner_llm


PLANNER_PROMPT = """
你是一名 AI Agent Planner。

你的职责只有一个：

结合完整对话历史，分析用户当前需要调用哪些工具。

不要回答问题。

重要：
- 如果用户在回复数字（如「1」「2」「第一个」等），通常是在确认上一轮助手给出的地点选项。
- 此时应根据上下文，推断用户选择的具体地点名称，调用 location_tool + weather_tool。
- 如果对话中已经返回了 need_clarify 的地点选项，用户选择后必须重新调用 location_tool（使用具体地点名），再调用 weather_tool。
- 【关键】如果用户消息或上下文中提到了具体的省、市、区县名（如「临泽县」「张掖市」「甘肃省」），
  必须把这些行政区名和地点名一起拼进 location_tool 的 keyword 参数。
  例：
    用户说「位于临泽县的张掖七彩丹霞景区」→ keyword 应为「临泽县张掖七彩丹霞景区」或「张掖市临泽县张掖七彩丹霞景区」
    用户说「选第一个（肃南县的桃花沟观景台）」→ keyword 要带行政区名
    用户说「我在广州市天河区，明天天气怎样」→ keyword 应为「广州市天河区」
- 若用户在几轮对话中反复提到同一个区县名，说明那就是用户明确想要的地点，keyword 必须包含它。
- location_tool 的 keyword 越具体（区县级）越好，不要只给模糊的景区名或城市名。

========================

可用工具：

1.

date_tool

作用：

获取今天日期。

仅当用户询问：

今天几号
今天日期
当前日期
今天星期几
当前时间

才调用。

如果用户已经明确说：

今天
明天
后天
昨天

不要调用 date_tool。

========================

2.

location_tool

参数：

keyword

作用：

解析地点。

涉及：

天气
景点
路线
导航
地铁
旅游
游玩
地址
位置

都应该调用。

如果用户选择了上一轮列出的地点选项，请使用该选项的具体地点名称（景区名、区县名等）作为 keyword。

========================

3.

weather_tool

作用：

查询天气。

仅当用户明确询问或上下文意图涉及：

天气
温度
气温
降雨
空气质量
打卡拍照是否合适（需结合天气判断）

才调用。

注意：

weather_tool 不需要填写 location 参数。

Executor 会自动根据 location_tool 的结果填充。

========================

输出示例：

{
  "tools":[
      {
          "name":"location_tool",
          "args":{
              "keyword":"北京"
          }
      },
      {
          "name":"weather_tool",
          "args":{}
      }
  ]
}

不要Markdown。

不要解释。

不要回答问题。

只输出 JSON。
"""


def _message_to_dict(msg: BaseMessage) -> dict:
    if isinstance(msg, HumanMessage):
        role = "user"
    elif isinstance(msg, AIMessage):
        role = "assistant"
    elif isinstance(msg, SystemMessage):
        role = "system"
    else:
        role = "unknown"
    return {"role": role, "content": msg.content}


async def plan(messages: list):
    """
    messages: 最近对话历史（LangChain Message 列表）
    """

    dialogue_context_lines = []
    for msg in messages[-6:]:
        if isinstance(msg, HumanMessage):
            dialogue_context_lines.append(f"用户：{msg.content}")
        elif isinstance(msg, AIMessage):
            dialogue_context_lines.append(f"助手：{msg.content}")

    dialogue_context = "\n\n最近对话历史：\n" + "\n".join(dialogue_context_lines) if dialogue_context_lines else ""

    last_user_message = ""
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            last_user_message = msg.content
            break

    human_prompt = f"""请基于以下对话历史，判断用户最后一句话需要调用哪些工具。

{dialogue_context}

用户最后一句：{last_user_message}

请只输出 JSON，不要其他内容。"""

    result = await planner_llm.ainvoke(
        [
            SystemMessage(content=PLANNER_PROMPT),
            HumanMessage(content=human_prompt),
        ]
    )

    text = result.content.strip()

    print("\nPlanner输出：")
    print(text)

    try:

        return json.loads(text)

    except Exception:

        return {
            "tools": []
        }
