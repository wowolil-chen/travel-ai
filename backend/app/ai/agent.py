import json

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)

from app.ai.executor import execute
from app.ai.model import llm
from app.ai.planner import plan
from app.ai.prompts import SYSTEM_PROMPT


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
    # 用户最后一句
    # ==========================

    last_user_message = ""

    for msg in reversed(history):

        if isinstance(msg, HumanMessage):

            last_user_message = msg.content

            break

    # ==========================
    # Planner
    # ==========================

    plan_result = await plan(last_user_message)

    print("\n==============================")
    print("Planner Result")
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