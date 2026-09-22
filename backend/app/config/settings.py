from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

DEEPSEEK_API_KEY = os.getenv(
    "DEEPSEEK_API_KEY"
)

TAVILY_API_KEY = os.getenv(
    "TAVILY_API_KEY"
)
# ==================== 项目路径配置 ====================

# backend 目录
BASE_DIR = Path(__file__).resolve().parents[2]

# 文档目录
DOCUMENTS_PATH = BASE_DIR / "data" / "documents"

# 向量数据库目录
VECTOR_DB_PATH = BASE_DIR / "data" / "vector_db"

# ==================== RAG相关配置 ====================
# Embedding模型
EMBEDDING_MODEL_NAME = "BAAI/bge-small-zh-v1.5"
# Reranker模型
RERANKER_MODEL_NAME = "BAAI/bge-reranker-base"
# 向量召回数量
RECALL_K = 15
# Reranker重排后返回数量
RERANK_TOP_K = 5
# Reranker最低分阈值
RERANK_SCORE_THRESHOLD = 0.5
# ==================== Web Search ====================

# Tavily 搜索返回结果数量
# 控制一次互联网搜索返回多少条网页资料
TAVILY_MAX_RESULTS = 3
# 单条网页内容最大保留字符数
# 用于限制搜索结果进入 LLM 上下文的文本长度，避免网页内容过长导致上下文膨胀
WEB_CONTENT_MAX_LENGTH = 800
