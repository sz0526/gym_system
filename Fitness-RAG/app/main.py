from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from app.rag import rag_pipeline_stream
from app.rag import rag_pipeline
import json

app = FastAPI()


class ChatRequest(BaseModel):
    question: str

# 普通接口
@app.post("/chat")
def chat(req: ChatRequest):
    answer = rag_pipeline(req.question)
    return {
        "answer": answer
    }


# 流式接口
@app.post("/chat/stream")
def chat_stream(req: ChatRequest):

    return StreamingResponse(
        rag_pipeline_stream(req.question),
        media_type="text/event-stream"  
    )