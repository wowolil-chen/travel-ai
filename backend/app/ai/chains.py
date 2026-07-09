from langchain_core.output_parsers import StrOutputParser

from app.ai.model import llm
from app.ai.prompts import travel_prompt

parser = StrOutputParser()

travel_chain = travel_prompt | llm | parser