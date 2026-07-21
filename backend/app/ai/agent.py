import json

from langchain_core.messages import (
    AIMessage,
    SystemMessage,
    ToolMessage,
)

from app.ai.model import llm
from app.ai.prompts import SYSTEM_PROMPT
from app.ai.tools import (
    date_tool,
    weather_tool,
    location_tool,
)

tool_map = {
    "date_tool": date_tool,
    "location_tool": location_tool,
    "weather_tool": weather_tool,
}


async def chat_with_tools(messages):
    """
    Agent

    User
      ↓
    LLM
      ↓
    Tool
      ↓
    LLM
      ↓
    Tool
      ↓
    ...
      ↓
    最终回答
    """

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *messages,
    ]

    while True:

        ai_message: AIMessage = await llm.ainvoke(messages)

        messages.append(ai_message)

        tool_calls = ai_message.tool_calls

        print("\n==============================")
        print("Tool Calls:")
        print(tool_calls)
        print("==============================\n")

        # 没有工具调用，结束循环
        if not tool_calls:
            break

        for tool_call in tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call.get("args", {})

            print(f"\n开始调用工具：{tool_name}")
            print(f"参数：{tool_args}")

            tool = tool_map.get(tool_name)

            if tool is None:

                result = {
                    "success": False,
                    "message": f"工具 {tool_name} 不存在。"
                }

            else:

                try:

                    result = tool.invoke(tool_args)

                    print("工具返回：")
                    print(result)

                except Exception as e:

                    print("工具异常：")
                    print(e)

                    result = {
                        "success": False,
                        "message": f"工具调用失败：{str(e)}"
                    }

            # ToolMessage 一律发送 JSON 字符串
            if isinstance(result, dict):

                tool_content = json.dumps(
                    result,
                    ensure_ascii=False
                )

            else:

                tool_content = str(result)

            messages.append(
                ToolMessage(
                    content=tool_content,
                    tool_call_id=tool_call["id"],
                )
            )

    print("\n开始最终回答...\n")

    async for chunk in llm.astream(messages):

        print(chunk)

        if getattr(chunk, "content", None):
            yield chunk.content