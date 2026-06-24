from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from app.rag import (
    rag_pipeline_stream,
    rag_pipeline,
    rag_pipeline_with_session,
    rag_pipeline_stream_with_session,
)
from app.session import session_store
from typing import Optional

app = FastAPI()


# ==========================
# 请求/响应模型
# ==========================
class ChatRequest(BaseModel):
    question: str
    enable_rerank: bool = False


class SessionChatRequest(BaseModel):
    session_id: str
    question: str
    n_rounds: int = 5
    enable_rerank: bool = False


class SessionResponse(BaseModel):
    session_id: str


class HistoryResponse(BaseModel):
    session_id: str
    messages: list
    total_rounds: int


# ==========================
# 无会话接口（向后兼容）
# ==========================
@app.post("/chat")
def chat(req: ChatRequest):
    answer = rag_pipeline(req.question)
    return {"answer": answer}


@app.post("/chat/stream")
def chat_stream(req: ChatRequest):
    return StreamingResponse(
        rag_pipeline_stream(req.question),
        media_type="text/event-stream"
    )


# ==========================
# 会话管理接口
# ==========================
@app.post("/session/create", response_model=SessionResponse)
def create_session():
    session_id = session_store.create_session()
    return {"session_id": session_id}


@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    deleted = session_store.delete_session(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="会话不存在")
    return {"status": "deleted", "session_id": session_id}


@app.get("/session/{session_id}/history", response_model=HistoryResponse)
def get_session_history(session_id: str):
    session = session_store.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="会话不存在")
    messages = [
        {"role": m.role, "content": m.content, "timestamp": m.timestamp}
        for m in session.messages
    ]
    total_rounds = len([m for m in session.messages if m.role == "user"])
    return {
        "session_id": session_id,
        "messages": messages,
        "total_rounds": total_rounds
    }


@app.delete("/session/{session_id}/history")
def clear_session_history(session_id: str):
    session = session_store.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="会话不存在")
    session.clear()
    return {"status": "cleared", "session_id": session_id}


@app.get("/session/list")
def list_sessions():
    return {"sessions": session_store.get_all_sessions()}


# ==========================
# 会话感知聊天接口
# ==========================
@app.post("/chat/session")
def chat_with_session(req: SessionChatRequest):
    try:
        answer = rag_pipeline_with_session(
            req.question,
            req.session_id,
            req.n_rounds
        )
        return {"answer": answer, "session_id": req.session_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/chat/session/stream")
def chat_stream_with_session(req: SessionChatRequest):
    try:
        return StreamingResponse(
            rag_pipeline_stream_with_session(
                req.question,
                req.session_id,
                req.n_rounds
            ),
            media_type="text/event-stream"
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))