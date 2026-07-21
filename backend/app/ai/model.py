from langchain_openai import ChatOpenAI

from app.ai.tools import (
    date_tool,
    location_tool,
    weather_tool,
)
from app.core.config import settings

# =========================
# Planner（负责规划）
# =========================

planner_llm = ChatOpenAI(
    model=settings.QWEN_MODEL,
    api_key=settings.QWEN_API_KEY,
    base_url=settings.QWEN_BASE_URL,
    temperature=0,
    streaming=False,
)

# =========================
# 最终回答（负责生成回复）
# =========================

llm = ChatOpenAI(
    model=settings.QWEN_MODEL,
    api_key=settings.QWEN_API_KEY,
    base_url=settings.QWEN_BASE_URL,
    temperature=0.7,
    streaming=True,
)

# =========================
# Tool Calling（兼容保留）
# 后面 executor 会直接调用工具，
# 这里保留 bind_tools 方便以后升级 LangGraph。
# =========================

tools = [
    date_tool,
    location_tool,
    weather_tool,
]

tool_llm = planner_llm.bind_tools(tools)