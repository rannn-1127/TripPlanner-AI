import re
from pathlib import Path
from functools import lru_cache

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.settings import DOCUMENTS_PATH, VECTOR_DB_PATH
from sentence_transformers import CrossEncoder



COLLECTION_NAME = "trip_planner"
EMBEDDING_MODEL_NAME = "BAAI/bge-small-zh-v1.5"
RERANKER_MODEL_NAME = "BAAI/bge-reranker-base"
_reranker = None


# ==================== Embedding ====================
@lru_cache(maxsize=1)
def get_embedding_model():
    """加载并获取 Embedding 模型"""
    print("加载Embedding模型")
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME
    )
@lru_cache(maxsize=1)
def get_reranker():
    """获取 Reranker 模型。"""
    global _reranker

    if _reranker is None:
        print("加载reranker模型...")
        _reranker = CrossEncoder(
            RERANKER_MODEL_NAME
        )

    return _reranker

# ==================== 文档加载 ====================

def load_document(file_path: str) -> list[Document]:
    """根据文件类型加载文档，并保存文件名"""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        loader = PyPDFLoader(str(path))
    elif suffix == ".docx":
        loader = Docx2txtLoader(str(path))
    elif suffix == ".txt":
        loader = TextLoader(str(path), encoding="utf-8")
    else:
        raise ValueError(f"暂不支持的文件类型: {suffix}")

    documents = loader.load()
    filename = path.name

    for doc in documents:
        doc.metadata["source"] = filename

    return documents


# ==================== 文档切分 ====================
def split_documents(
    documents: list[Document]
) -> list[Document]:
    """
    按页面进行结构化切分。
    页面内优先按照景点/章节切分，
    超过 500 字的内容再使用递归字符切分。
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=[
            "\n\n",
            "\n",
            "。",
            "，",
            " "
        ]
    )
    chunks = []

    for document in documents:
        text = document.page_content.strip()

        if not text:
            continue

        # 当前页面的基础 metadata
        base_metadata = document.metadata.copy()

        # 按“数字 + . / 、”形式的章节标题切分
        sections = re.split(
            r"(?=\n?\d+[、.．]\s*)",
            text
        )

        for section in sections:
            section = section.strip()

            if not section:
                continue
            # 提取章节/景点名称
            match = re.match(
                r"(\d+)[、.．]\s*(.+?)(?:\n|$)",
                section
            )

            metadata = base_metadata.copy()

            if match:
                metadata["title"] = match.group(2).strip()

            # 不超过 500 字，直接作为一个 Chunk
            if len(section) <= 500:
                chunks.append(
                    Document(
                        page_content=section,
                        metadata=metadata
                    )
                )
                continue

            # 超过 500 字，再递归切分
            sub_chunks = splitter.split_text(section)

            for index, sub_chunk in enumerate(sub_chunks):
                sub_metadata = metadata.copy()
                sub_metadata["chunk_index"] = index

                chunks.append(
                    Document(
                        page_content=sub_chunk,
                        metadata=sub_metadata
                    )
                )

    return chunks


# ==================== 向量数据库 ====================
def get_vectorstore() -> Chroma:
    """加载已有向量数据库。"""
    embedding_model = get_embedding_model()

    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(VECTOR_DB_PATH),
        embedding_function=embedding_model
    )


def create_vector_store(chunks: list[Document]) -> Chroma:
    """第一次创建向量数据库。"""
    embedding_model = get_embedding_model()

    return Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=COLLECTION_NAME,
        persist_directory=str(VECTOR_DB_PATH)
    )


# ==================== 文档管理 ====================

def document_exists(filename: str) -> bool:
    """判断文件是否已经存在于知识库。"""
    if not VECTOR_DB_PATH.exists():
        return False

    vectorstore = get_vectorstore()

    result = vectorstore.get(
        where={"source": filename},
        limit=1
    )
    return len(result["ids"]) > 0


def add_document(file_path: str) -> dict:
    """
    加载并添加一个新文档。
    如果文件已经存在，则拒绝重复添加。
    """
    filename = Path(file_path).name

    if document_exists(filename):
        return {
            "success": False,
            "message": f"文件已经存在: {filename}"
        }

    documents = load_document(file_path)
    chunks = split_documents(documents)

    if VECTOR_DB_PATH.exists():
        vectorstore = get_vectorstore()
        vectorstore.add_documents(chunks)
    else:
        vectorstore = create_vector_store(chunks)

    return {
        "success": True,
        "message": f"文档添加成功: {filename}",
        "filename": filename,
        "document_count": len(documents),
        "chunk_count": len(chunks)
    }


def delete_document(filename: str) -> dict:
    """根据文件名删除文档对应的所有向量。"""
    if not VECTOR_DB_PATH.exists():
        return {
            "success": False,
            "message": "向量数据库不存在"
        }

    vectorstore = get_vectorstore()

    result = vectorstore.get(
        where={"source": filename},
        limit=1
    )

    if not result["ids"]:
        return {
            "success": False,
            "message": f"文件不存在: {filename}"
        }

    vectorstore.delete(
        where={"source": filename}
    )

    return {
        "success": True,
        "message": f"文档删除成功: {filename}"
    }


def list_documents() -> list[str]:
    """获取知识库中的所有文件名。"""
    if not VECTOR_DB_PATH.exists():
        return []

    vectorstore = get_vectorstore()

    result = vectorstore.get()

    filenames = {
        metadata.get("source")
        for metadata in result["metadatas"]
        if metadata.get("source")
    }

    return sorted(filenames)


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

    vectorstore = get_vectorstore()
    # ---------- 第一阶段：向量召回 ----------

    recall_results = vectorstore.similarity_search_with_score(
        query,
        k=recall_k
    )

    if not recall_results:
        return []

    # ---------- 第二阶段：Reranker 重排 ----------
    reranker = get_reranker()

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


# ==================== 测试 ====================

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