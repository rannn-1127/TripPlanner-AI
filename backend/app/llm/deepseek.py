from langchain_openai import ChatOpenAI

from app.config.settings import DEEPSEEK_API_KEY

"""
获取 DeepSeek LLM
"""


def get_deepseek_llm():
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com",
        temperature=0.3,
        timeout=30,
        max_retries=2#一次ds请求最多等待30秒，失败自动重试2次
    )
    return llm
