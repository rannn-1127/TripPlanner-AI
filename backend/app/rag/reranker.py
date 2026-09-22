import threading
from sentence_transformers import CrossEncoder
from app.config.settings import RERANKER_MODEL_NAME

_reranker = None

_reranker_lock = threading.Lock()

# ==================== reranker ====================
def get_reranker_model():
    """获取 Reranker 模型"""
    global _reranker

    if _reranker is None:
        with _reranker_lock:
            if _reranker is None:
                print("初始化Reranker模型...")

                _reranker = CrossEncoder(
                    RERANKER_MODEL_NAME
                )

    return _reranker