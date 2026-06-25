import os
from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import operator
import requests

from app.config import DASHSCOPE_API_KEY

# ========================
# 1. 定义工具（用装饰器方式）
# ========================

@tool
def get_member_classes(member_account: str) -> str:
    """查询会员已报名的课程。当用户问自己报名了哪些课程、明天有没有课时使用。传入会员账号数字字符串。"""
    try:
        resp = requests.get(
            "http://localhost:8080/api/class/getClassByMember",
            params={"memberAccount": member_account.strip()},
            timeout=5
        )
        data = resp.json()
        if not data.get("success"):
            return "查询失败"
        orders = data.get("orders", [])
        if not orders:
            return "该会员暂无报名课程"
        result = []
        for o in orders:
            result.append(
                f"课程：{o.get('className')}，"
                f"教练：{o.get('coach')}，"
                f"上课时间：{o.get('classBegin')}"
            )
        return "\n".join(result)
    except Exception as e:
        return f"查询异常：{str(e)}"


@tool
def get_all_classes(query: str = "") -> str:
    """查询健身房所有可报名课程。当用户问有哪些课程可以报名时使用。"""
    try:
        resp = requests.get(
            "http://localhost:8080/api/class/getAllClass",
            timeout=5
        )
        data = resp.json()
        if not data.get("success"):
            return "查询失败"
        classList = data.get("classList", [])
        if not classList:
            return "暂无课程信息"
        result = []
        for c in classList:
            result.append(
                f"课程：{c.get('className')}，"
                f"教练：{c.get('coach')}，"
                f"上课时间：{c.get('classBegin')}，"
                f"课程时长：{c.get('classTime', '未知')}"
            )
        return "\n".join(result)
    except Exception as e:
        return f"查询异常：{str(e)}"


@tool
def get_gym_info(query: str = "") -> str:
    """查询健身房基本信息，包括营业时间、地址、联系方式。"""
    return (
        "营业时间：周一至周日 06:00-22:00\n"
        "地址：xx市xx区xx路xx号\n"
        "联系电话：400-xxx-xxxx"
    )


tools = [get_member_classes, get_all_classes, get_gym_info]

# ========================
# 2. 定义 LLM
# ========================

llm = ChatOpenAI(
    model="qwen-plus",
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.1,
    streaming=False
).bind_tools(tools)  # 绑定工具

# ========================
# 3. 定义状态
# ========================

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

# ========================
# 4. 定义节点
# ========================

SYSTEM_PROMPT = """你是一个专业的健身房AI助手，可以回答健身知识问题，也可以查询课程、营业时间等信息。
查询会员课程时需要传入会员账号。
请用中文回答。"""

def call_llm(state: AgentState) -> AgentState:
    """调用 LLM 节点"""
    from langchain_core.messages import SystemMessage
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def should_continue(state: AgentState) -> str:
    """判断是否继续调用工具"""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END


# ========================
# 5. 构建图
# ========================

tool_node = ToolNode(tools)

graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("tools", tool_node)

graph.set_entry_point("llm")
graph.add_conditional_edges("llm", should_continue)
graph.add_edge("tools", "llm")  # 工具执行完回到 LLM 继续推理

app_graph = graph.compile()


# ========================
# 6. 对外调用函数
# ========================

def run_agent(question: str, member_account: str = "") -> str:
    full_question = question
    if member_account:
        full_question = f"{question}（会员账号：{member_account}）"
    try:
        result = app_graph.invoke({
            "messages": [HumanMessage(content=full_question)]
        })
        last_message = result["messages"][-1]
        return last_message.content
    except Exception as e:
        return f"处理失败：{str(e)}"