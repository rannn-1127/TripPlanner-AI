from app.config.settings import DOCUMENTS_PATH, VECTOR_DB_PATH
from app.rag.vector_store import get_vector_store
from app.rag.reranker import get_reranker_model
# ==================== 召回 + 重排 ====================

def search_documents(
    query: str,
    recall_k: int = 15,
    top_k: int = 5
) -> list[dict]:
    """
    先通过向量检索召回候选文档，
    再通过 CrossEncoder Reranker 进行重排。
    """
    if not VECTOR_DB_PATH.exists():
        return []

    vectorstore = get_vector_store()
    # ---------- 第一阶段：向量召回 ----------
    recall_results = vectorstore.similarity_search_with_score(
        query,
        k=recall_k
    )

    if not recall_results:
        return []

    # ---------- 第二阶段：Reranker 重排 ----------
    reranker = get_reranker_model()

    pairs = [
        [query, document.page_content]
        for document, _ in recall_results
    ]

    rerank_scores = reranker.predict(pairs)

    # 将文档和重排分数组合
    results = []

    for (document, recall_score), rerank_score in zip(
        recall_results,
        rerank_scores
    ):
        results.append({
            "content": document.page_content,
            "source": document.metadata.get("source"),
            "page": document.metadata.get("page"),
            "recall_score": float(recall_score),
            "rerank_score": float(rerank_score)
        })

    # 按 Reranker 分数从高到低排序
    results.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    # 返回重排后的 Top-K
    return results[:top_k]
