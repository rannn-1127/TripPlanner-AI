from langchain_core.tools import tool
from app.rag.rag import search_documents as rag_search_documents


@tool
def search_documents(query: str) -> str:
    """
    从本地知识库检索目的地旅游资料。
    适用于查询景点介绍、交通路线、游玩建议、注意事项等信息。
    参数：query - 搜索关键词，如"上海夜景景点"
    """
    try:
        results = rag_search_documents(
            query,
            recall_k=15,
            top_k=5
        )

        if not results:
            return "知识库中未找到相关目的地资料。"

        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(
                f"[资料{i}] {r['content']}\n"
                f"来源：{r['source']}\n"
                f"链接：无\n"
                f"页码：{r['page']}"
            )

        return "\n\n".join(formatted)

    except Exception as e:
        return f"本地知识库查询失败：{str(e)}"


if __name__ == "__main__":
    result = search_documents.invoke(
        {
            "query": "上海有哪些适合晚上游玩的景点？"
        }
    )
    print(result)