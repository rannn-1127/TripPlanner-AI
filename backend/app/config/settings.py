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