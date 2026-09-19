import threading

from langchain.agents import create_agent

from app.llm.deepseek import get_deepseek_llm
from app.tools.rag_tool import search_documents
from app.tools.search_web import search_web

from app.agent.prompts import TRIP_PLANNER_AGENT_PROMPT


_agent = None
_agent_lock = threading.Lock()


def get_trip_agent():
    """
    获取旅行规划 Agent 单例
    """
    global _agent

    if _agent is None:
        with _agent_lock:

            if _agent is None:
                llm = get_deepseek_llm()
                print("加载agent")
                tools = [
                    search_documents,
                    search_web
                ]

                _agent = create_agent(
                    model=llm,
                    tools=tools,
                    system_prompt=TRIP_PLANNER_AGENT_PROMPT
                )

    return _agent