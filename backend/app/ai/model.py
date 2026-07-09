from langchain_openai import ChatOpenAI

from app.core.config import settings

llm = ChatOpenAI(
    model=settings.QWEN_MODEL,
    api_key=settings.QWEN_API_KEY,
    base_url=settings.QWEN_BASE_URL,
    temperature=0.7,
    streaming=False,
)