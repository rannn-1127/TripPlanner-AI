from langchain_core.tools import tool
from tavily import TavilyClient
from app.config.settings import TAVILY_API_KEY
from functools import lru_cache
import re

@lru_cache(maxsize=1)
def get_tavily_client():
    print("初始化 Tavily Client")
    return TavilyClient(
        api_key=TAVILY_API_KEY
    )

def clean_text(text: str) -> str:
    """
    清洗网页搜索结果
    """
    if not text:
        return ""
    # 去除多余空白
    text = re.sub(r"\s+", " ", text)
    # 去除特殊符号
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

    return text.strip()


@tool
def search_web(query: str) -> str:
    """
    搜索互联网中的旅游信息。
    适用于查询景点介绍、交通路线、开放时间、游玩建议等实时信息。

    参数：
    query - 搜索关键词，例如：
    "上海外滩最佳游玩时间"
    "杭州西湖交通路线"
    """
    try:
        client = get_tavily_client()
        response = client.search(
            query=query,
            max_results=5,
            search_depth="advanced"
        )

        results = response.get("results", [])

        if not results:
            return "互联网中未找到相关旅游资料。"

        formatted = []

        for i, item in enumerate(results, 1):
            content = clean_text(
                item.get("content", "")
            )

            # 限制长度，避免上下文爆炸
            if len(content) > 1500:
                content = content[:1500] + "..."

            formatted.append(
                f"[资料{i}] {content}\n"
                f"来源：互联网搜索\n"
                f"链接：{item.get('url', '无')}\n"
                f"页码：无"
            )

        return "\n\n".join(formatted)


    except Exception as e:
        return f"互联网搜索失败：{str(e)}"



if __name__ == "__main__":

    result = search_web.invoke(
        {
            "query": "上海外滩最佳游玩时间和交通路线"
        }
    )

    print(result)