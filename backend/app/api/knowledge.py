from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
from pathlib import Path
from app.config.settings import DOCUMENTS_PATH
from app.rag.knowledge import (
    add_document,
    delete_document,
    list_documents
)

#创建路由器对象
router = APIRouter(
    prefix="/knowledge",
    tags=["knowledge"]
)
# 限制上传文件类型
ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):
    """
    上传旅游资料并构建知识库。
    """
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="文件名不能为空"
        )
    # 提取文件名和后缀防止上传恶意文件
    filename = Path(file.filename).name
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="暂不支持该文件类型，仅支持 PDF、DOCX、TXT"
        )

    # 上传文件前确保目录存在
    DOCUMENTS_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = DOCUMENTS_PATH / file.filename

    # 保存文件 把上传的文件流式写入磁盘
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )#shutil.copyfileobj 做分块复制，避免大文件一次性加载到内存里

    # 加载文档、切分并写入向量数据库
    result = add_document(str(file_path))

    # 如果文档已存在，删除刚上传的重复文件
    if not result["success"]:
        file_path.unlink(missing_ok=True)#如果文件不存在也不报错，静默跳过

    return result


@router.get("/files")
def get_files():
    """
    获取知识库中的文件列表。
    """
    return {"files": list_documents()}


@router.delete("/file/{filename}")
def delete_file(filename: str):
    """
    删除文档及其对应的向量数据。
    """
    file_path = DOCUMENTS_PATH / filename
    # 删除本地文档
    file_path.unlink(missing_ok=True)
    # 删除 Chroma 中对应的向量
    result = delete_document(filename)

    return result