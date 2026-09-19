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

        temperature=0.3

    )
    return llm