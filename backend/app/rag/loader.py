# 文档加载

from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader
)
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