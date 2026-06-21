from langchain_openai import ChatOpenAI
from app.config import DASHSCOPE_API_KEY


def get_stream_llm():

    return ChatOpenAI(
        model="qwen-plus",
        api_key=DASHSCOPE_API_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        temperature=0.3,
        streaming=True,
    )