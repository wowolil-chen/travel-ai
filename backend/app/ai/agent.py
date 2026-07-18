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
)

tool_map = {
    "date_tool": date_tool,
    "weather_tool": weather_tool,
}


async def chat_with_tools(messages):
    """
    Agent

    流程：

    User
      ↓
    LLM
      ↓
    判断是否调用 Tool
      ↓
    Tool
      ↓
    LLM
      ↓
    如果还有 Tool 继续循环
      ↓
    最终 Streaming 输出
    """

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *messages,
    ]

    # Tool Calling 循环
    while True:

        ai_message: AIMessage = await llm.ainvoke(messages)

        messages.append(ai_message)

        tool_calls = ai_message.tool_calls

        # ===== 调试输出 =====
        print("\n==============================")
        print("Tool Calls:")
        print(tool_calls)
        print("==============================\n")

        # 没有 Tool，结束循环
        if not tool_calls:
            break

        # 执行所有 Tool
        for tool_call in tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call.get("args", {})

            print(f"\n开始调用工具：{tool_name}")
            print(f"参数：{tool_args}")

            tool = tool_map.get(tool_name)

            if tool is None:

                result = f"工具 {tool_name} 不存在。"

            else:

                try:

                    result = tool.invoke(tool_args)

                    print("工具返回：")
                    print(result)

                except Exception as e:

                    print("工具异常：")
                    print(e)

                    result = f"工具 {tool_name} 调用失败：{str(e)}"

            messages.append(
                ToolMessage(
                    content=result,
                    tool_call_id=tool_call["id"],
                )
            )

    print("\n开始最终回答...\n")

    # Tool 全部执行完成，再流式输出最终回答
    async for chunk in llm.astream(messages):

        if chunk.content:
            yield chunk.content