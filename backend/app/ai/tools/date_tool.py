from datetime import datetime

from langchain.tools import tool


@tool
def date_tool() -> str:
    """
    获取当前日期。
    """

    return datetime.now().strftime("%Y-%m-%d")