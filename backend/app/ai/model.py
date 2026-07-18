from langchain_openai import ChatOpenAI

from app.ai.tools.date_tool import date_tool
from app.ai.tools.weather_tool import weather_tool
from app.core.config import settings

llm = ChatOpenAI(
    model=settings.QWEN_MODEL,
    api_key=settings.QWEN_API_KEY,
    base_url=settings.QWEN_BASE_URL,
    temperature=0.7,
    streaming=True,
)

tools = [
    weather_tool,
    date_tool,
]

llm = llm.bind_tools(tools)