from pathlib import Path

from app.config.settings import VECTOR_DB_PATH

from app.rag.loader import load_document
from app.rag.splitter import split_documents
from app.rag.vector_store import (
    get_vector_store,
    create_vector_store
)
# ==================== 文档管理 ====================

def document_exists(filename: str) -> bool:
    """判断文件是否已经存在于知识库。"""
    if not VECTOR_DB_PATH.exists():
        return False

    vectorstore = get_vector_store()

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
        vectorstore = get_vector_store()
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
    """根据文件名删除文档对应的所有向量"""
    if not VECTOR_DB_PATH.exists():
        return {
            "success": False,
            "message": "向量数据库不存在"
        }

    vectorstore = get_vector_store()

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

    vectorstore = get_vector_store()

    result = vectorstore.get()

    filenames = {
        metadata.get("source")
        for metadata in result["metadatas"]
        if metadata.get("source")
    }

    return sorted(filenames)