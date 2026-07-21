from datetime import datetime

from langchain.tools import tool


@tool
async def date_tool() -> str:
    """
    返回今天日期。
    """

    return datetime.now().strftime("%Y-%m-%d")