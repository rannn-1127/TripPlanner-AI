# ==================== 测试RAG ====================
from app.config.settings import DOCUMENTS_PATH
from app.rag.knowledge import add_document,list_documents
from app.rag.rag import search_documents

if __name__ == "__main__":
    pdf_path = DOCUMENTS_PATH / "上海景点资料.pdf"

    # 添加文档
    result = add_document(str(pdf_path))
    print("文档添加:")
    print(result)

    # 查看知识库
    print("\n当前知识库:")
    for filename in list_documents():
        print("-", filename)

    # 检索 + 重排测试
    queries = [
        "上海有哪些适合晚上游玩的景点？",
        "上海有哪些历史文化景点？",
        "上海有哪些适合亲子游的景点？"
    ]

    for query in queries:
        print("\n" + "=" * 60)
        print(f"问题：{query}")
        print("=" * 60)

        results = search_documents(
            query=query,
            recall_k=15,
            top_k=5
        )

        if not results:
            print("知识库中没有找到相关信息。")
            continue

        for i, result in enumerate(results):
            print(f"\n--- 重排结果 {i + 1} ---")
            print("内容:")
            print(result["content"])
            print("来源:", result["source"])
            print("页码:", result["page"])
            print("召回距离:", result["recall_score"])
            print("重排分数:", result["rerank_score"])