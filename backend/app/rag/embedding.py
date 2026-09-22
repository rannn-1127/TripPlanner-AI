import threading
from langchain_huggingface import HuggingFaceEmbeddings
from app.config.settings import EMBEDDING_MODEL_NAME

_embedding_model = None

_embedding_lock = threading.Lock()

# ==================== Embedding ====================

def get_embedding_model():
    """加载并获取 Embedding 模型"""
    global _embedding_model
    if _embedding_model is None:
        with _embedding_lock:
            if _embedding_model is None:
                print("初始化Embedding模型")

                _embedding_model = HuggingFaceEmbeddings(
                    model_name=EMBEDDING_MODEL_NAME
                )

    return _embedding_model