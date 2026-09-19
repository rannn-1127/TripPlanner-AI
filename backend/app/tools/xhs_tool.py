from langchain_core.tools import tool
from tavily import TavilyClient

from app.config.settings import TAVILY_API_KEY


# 小红书旅游相关关键词
XHS_KEYWORDS = [
    "旅游",
    "旅行",
    "攻略",
    "景点",
    "路线",
    "游玩",
    "行程",
    "美食",
    "citywalk",
    "避坑",
    "打卡",
]


def is_relevant(result: dict) -> bool:
    """判断小红书结果是否与旅游攻略相关。"""
    title = result.get("title", "")
    content = result.get("content", "")

    text = f"{title} {content}".lower()

    return any(
        keyword.lower() in text
        for keyword in XHS_KEYWORDS
    )


@tool
def search_xhs(query: str) -> str:
    """
    搜索小红书旅游攻略。
    用于获取游客实际游玩体验、旅游路线、美食推荐、
    景点打卡和避坑建议等内容。
    """
    try:
        client = TavilyClient(
            api_key=TAVILY_API_KEY
        )

        # 限定搜索小红书
        response = client.search(
            query=f"site:xiaohongshu.com {query} 旅游攻略",
            max_results=8
        )

        results = response.get("results", [])

        if not results:
            return "未找到相关小红书攻略。"

        # 只保留小红书链接
        results = [
            result
            for result in results
            if "xiaohongshu.com" in result.get("url", "")
        ]

        if not results:
            return "未找到相关小红书攻略。"

        # 过滤不相关内容
        results = [
            result
            for result in results
            if is_relevant(result)
        ]

        if not results:
            return "未找到与旅游需求相关的小红书攻略。"

        # 按 Tavily 相关性分数排序
        results.sort(
            key=lambda x: x.get("score", 0),
            reverse=True
        )

        # 最终只返回 Top 5
        results = results[:5]

        formatted = []

        for i, result in enumerate(results, 1):
            formatted.append(
                f"[资料{i}]\n"
                f"来源：{result.get('title', '小红书旅游攻略')}\n"
                f"链接：{result.get('url', '无')}\n"
                f"内容：{result.get('content', '')}"
            )
        return "\n\n".join(formatted)

    except Exception as e:
        return f"小红书搜索失败：{str(e)}"


if __name__ == "__main__":
    print(search_xhs.invoke("上海3天旅游攻略"))