from langchain_core.tools import tool
from app.rag.rag import search_documents as rag_search_documents
from app.config.settings import RECALL_K,RERANK_TOP_K

@tool
def search_documents(query: str) -> str:
    """
    查询本地旅游知识库，获取用户上传的目的地资料。

    用于获取：
    - 景点介绍
    - 交通路线
    - 游玩建议
    - 美食推荐
    - 注意事项
    规划旅游行程时应优先使用该工具。
    参数:
        query: 需要查询的旅游主题，例如"上海夜景景点"
    """
    try:
        results = rag_search_documents(
            query,
            recall_k=RECALL_K,
            top_k=RERANK_TOP_K
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
        print("使用RAG_tool")
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