from fastapi import APIRouter
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from app.agent.agent import get_trip_agent
from app.storage.trip_storage import save_trip
from langchain_core.messages import ToolMessage

router = APIRouter(
    prefix="/trip",
    tags=["trip"]
)

agent=None
def get_agent():
    global agent
    if agent is None:
        agent=get_trip_agent()
    return agent

class TripRequest(BaseModel):
    destination: str
    days: int
    interests: list[str]
    pace: str

@router.post("/stream")
async def create_trip(request: TripRequest):
    """
    根据游客偏好生成旅游行程，并通过 SSE 流式返回。
    """
    query = f"""
目的地：{request.destination}
游玩天数：{request.days}天
兴趣偏好：{", ".join(request.interests)}
行程节奏：{request.pace}

请根据以上信息规划旅游行程。
"""

    # SSE事件生成器
    # 通过yield不断向前端发送数据
    async def event_generator():
        # 缓存LLM输出
        # 因为模型是token级输出
        # 不适合每个token发送
        buffer = ""
        full_content = "" # 负责保存完整攻略
        answer_started = False# 是否进入正式报告阶段
        # 初始状态
        yield {
            "event": "thinking",
            "data": "开始分析需求..."
        }
        # 调用Agent流式执行
        async for chunk in get_agent().astream(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": query
                        }
                    ]
                },
                stream_mode=[
                    "messages",# LLM 逐 token 输出的消息
                    "updates"# Agent 状态更新
                ]
        ):
            mode, data = chunk#mode：表示当前这条数据属于哪一种流;data：具体的数据内容
            # =========================
            # 处理模型输出
            # =========================
            if mode == "messages":
                message, metadata = data
                # 过滤空消息
                # ToolMessage 是工具返回结果，不应该展示给用户
                if isinstance(message, ToolMessage):
                    continue

                if message.content:
                    buffer += message.content
                    # ---------------------
                    # 等待报告开始
                    # ---------------------
                    if not answer_started:
                        # 判断正式的攻略标志
                        if (
                                "# " in buffer
                                or "## " in buffer
                                or "旅游行程" in buffer
                        ):
                            answer_started = True
                            full_content += buffer
                            yield {
                                "event": "message",
                                "data": buffer
                            }
                            buffer = ""
                        # 丢弃Agent前置说明
                        elif len(buffer) > 300:
                            buffer = ""
                    # ---------------------
                    # 输出正式攻略
                    # ---------------------
                    else:
                        # 累积一定长度再发送
                        # 避免页面疯狂刷新
                        if len(buffer) >= 30:
                            full_content += buffer #保存完整攻略
                            yield {
                                "event": "message",
                                "data": buffer
                            }
                            buffer = ""
            # =========================
            # Agent状态
            # =========================
            elif mode == "updates":
                if "tools" in data:
                    messages = data["tools"]["messages"]
                    for msg in messages:
                        yield {
                            "event": "thinking",
                            "data": f"正在调用工具:{msg.name}"
                        }


        # 输出剩余内容
        if buffer and answer_started:
            full_content += buffer  # 保存完整攻略
            yield {
                "event": "message",
                "data": buffer
            }
        # 保存历史记录
        trip_id = save_trip(
            destination=request.destination,
            days=request.days,
            interests=request.interests,
            pace=request.pace,
            content=full_content
        )
        yield {
            "event": "trip_id",
            "data": str(trip_id)
        }
        # 完成状态
        yield {
            "event": "thinking",
            "data": "行程生成完成"
        }
        print("生成完成")
        # 前端关闭连接
        yield {
            "event": "done",
            "data": ""
        }

    return EventSourceResponse(
        event_generator()
    )