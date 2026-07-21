import json

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from app.ai.model import planner_llm


PLANNER_PROMPT = """
你是一名 AI Agent Planner。

你的职责只有一个：

分析用户需要调用哪些工具。

不要回答问题。

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

========================

3.

weather_tool

作用：

查询天气。

仅当用户明确询问：

天气
温度
气温
降雨
空气质量

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


async def plan(user_message: str):

    result = await planner_llm.ainvoke(
        [
            SystemMessage(content=PLANNER_PROMPT),
            HumanMessage(content=user_message),
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