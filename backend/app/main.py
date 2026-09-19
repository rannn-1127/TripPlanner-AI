from fastapi import FastAPI

from app.api.trip import router as trip_router
from app.api.knowledge import router as knowledge_router
from app.api.history import router as history_router
from app.api.export import router as export_router

# 应用入口（启动整个 FastAPI 服务）
app = FastAPI(
    title="TripPlanner-AI"
)

from fastapi.middleware.cors import CORSMiddleware
# ==============================
# CORS跨域配置
# ==============================
# 需要允许Vue访问后端
app.add_middleware(
    CORSMiddleware,
    # 允许哪些前端地址访问
    allow_origins=[
        "http://localhost:5173"
    ],
    # 是否允许携带cookie
    allow_credentials=True,
    # 允许GET POST PUT DELETE等请求
    allow_methods=[
        "*"
    ],
    # 允许所有请求头
    allow_headers=[
        "*"
    ]
)


# ==============================
# 注册 API 路由
# ==============================
app.include_router(trip_router)
app.include_router(knowledge_router)
app.include_router(history_router)
app.include_router(export_router)