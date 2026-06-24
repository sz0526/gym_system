from app.retriever import get_hybrid_retriever
from app.prompt import RAG_PROMPT, build_dynamic_prompt
from app.llm import get_llm
from app.reranker import BGEReranker
from app.session import session_store, build_context_from_history
from typing import Optional
import time


# ==========================
# 重排序器单例（懒加载）
# ==========================
_reranker: Optional[BGEReranker] = None

# 配置本地模型路径（离线环境使用）
# 如果设置了本地路径，会优先使用本地模型，且不尝试联网下载
LOCAL_RERANKER_MODEL_PATH = None  # 设置为本地模型目录路径，如 "./models/bge-reranker-v2-m3"

def _get_reranker() -> BGEReranker:
    global _reranker
    if _reranker is None:
        _reranker = BGEReranker(
            model_name="BAAI/bge-reranker-v2-m3",
            local_model_path=LOCAL_RERANKER_MODEL_PATH
        )
    return _reranker


# ==========================
# 检索 + 重排序
# ==========================
def _retrieve_and_rerank(
    question: str,
    initial_k: int = 6,
    top_k: int = 3,
    enable_rerank: bool = False
):
    retriever = get_hybrid_retriever(k=initial_k)
    docs = retriever.invoke(question)

    if enable_rerank and len(docs) > top_k:
        doc_texts = [doc.page_content for doc in docs]
        reranker = _get_reranker()
        ranked = reranker.rerank(question, doc_texts, top_k=top_k)
        docs = [docs[idx] for idx, _, _ in ranked]

    return docs


# ==========================
# 普通聊天（无会话）
# ==========================
def rag_chat(question: str, enable_rerank: bool = True):
    docs = _retrieve_and_rerank(question, enable_rerank=enable_rerank)

    print("=" * 50)
    print("检索到文档数量：", len(docs))
    for i, doc in enumerate(docs):
        print(f"\n------ Document {i + 1} ------")
        print(doc.page_content[:300])

    context = "\n\n".join(doc.page_content for doc in docs)
    print("=" * 50)
    print("Retrieved Context:")
    print(context)
    print("=" * 50)

    llm = get_llm()
    prompt = RAG_PROMPT.invoke({"context": context, "question": question})
    response = llm.invoke(prompt)
    return response.content


# ==========================
# 流式聊天（无会话）
# ==========================
def rag_chat_stream(question: str, enable_rerank: bool = False):
    docs = _retrieve_and_rerank(question, enable_rerank=enable_rerank)

    context = "\n\n".join(doc.page_content for doc in docs)
    llm = get_llm(streaming=True)
    prompt = RAG_PROMPT.invoke({"context": context, "question": question})

    for chunk in llm.stream(prompt):
        if chunk.content:
            yield f"data: {chunk.content}\n\n"


# ==========================
# 会话感知聊天（普通）
# ==========================
def rag_chat_with_session(
    question: str,
    session_id: str,
    n_rounds: int = 5,
    enable_rerank: bool = False
):
    session = session_store.get_session(session_id)
    if session is None:
        raise ValueError(f"会话不存在: {session_id}")

    # 1. 检索 + 重排序
    docs = _retrieve_and_rerank(question, enable_rerank=enable_rerank)

    print("=" * 50)
    print(f"[Session {session_id}] 检索到文档数量：", len(docs))
    for i, doc in enumerate(docs):
        print(f"\n------ Document {i + 1} ------")
        print(doc.page_content[:300])

    context = "\n\n".join(doc.page_content for doc in docs)

    # 2. 构建对话历史上下文
    history_msgs = session.get_history(max_rounds=n_rounds)
    history_str = build_context_from_history(history_msgs, max_tokens=2000)

    # 3. 动态 Prompt
    prompt = build_dynamic_prompt(
        context=context,
        question=question,
        history=history_str,
        n_rounds=n_rounds
    )

    # 4. 调用 LLM
    llm = get_llm()
    response = llm.invoke(prompt)
    answer = response.content

    # 5. 存入会话历史
    session.add_message("user", question)
    session.add_message("assistant", answer)

    return answer


# ==========================
# 会话感知聊天（流式）
# ==========================
def rag_chat_stream_with_session(
    question: str,
    session_id: str,
    n_rounds: int = 5,
    enable_rerank: bool = False
):
    session = session_store.get_session(session_id)
    if session is None:
        raise ValueError(f"会话不存在: {session_id}")

    docs = _retrieve_and_rerank(question, enable_rerank=enable_rerank)

    context = "\n\n".join(doc.page_content for doc in docs)

    history_msgs = session.get_history(max_rounds=n_rounds)
    history_str = build_context_from_history(history_msgs, max_tokens=2000)

    prompt = build_dynamic_prompt(
        context=context,
        question=question,
        history=history_str,
        n_rounds=n_rounds
    )

    llm = get_llm(streaming=True)

    # 收集完整回复用于存入历史
    full_answer = []

    for chunk in llm.stream(prompt):
        if chunk.content:
            full_answer.append(chunk.content)
            yield f"data: {chunk.content}\n\n"

    session.add_message("user", question)
    session.add_message("assistant", "".join(full_answer))


# ==========================
# Pipeline（向后兼容）
# ==========================
def rag_pipeline(question: str):
    return rag_chat(question)


def rag_pipeline_stream(question: str):
    return rag_chat_stream(question)


def rag_pipeline_with_session(question: str, session_id: str, n_rounds: int = 5):
    return rag_chat_with_session(question, session_id, n_rounds)


def rag_pipeline_stream_with_session(question: str, session_id: str, n_rounds: int = 5):
    return rag_chat_stream_with_session(question, session_id, n_rounds)