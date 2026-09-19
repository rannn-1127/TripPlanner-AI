from pathlib import Path

"""
获得项目的根目录
"""
def find_project_root():
    current = Path(__file__).resolve()

    for parent in current.parents:
        if (parent / "pyproject.toml").exists():
            return parent

    raise RuntimeError("找不到项目根目录")


BASE_DIR = find_project_root()


VECTOR_DB_PATH = (
    BASE_DIR /
    "data" /
    "vector_db"
)