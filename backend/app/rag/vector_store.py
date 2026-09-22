# 向量数据库
from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.config.settings import (
    VECTOR_DB_PATH
)
from app.rag.embedding import get_embedding_model


COLLECTION_NAME="trip_planner"

def get_vector_store() -> Chroma:
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