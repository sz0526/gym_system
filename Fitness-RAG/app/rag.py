from app.retriever import get_hybrid_retriever
from app.prompt import RAG_PROMPT
from app.llm import get_llm
import time
import re


# ==========================
# 普通聊天（一次性返回）
# ==========================
def rag_chat(question: str):

    # 1. 初始化
    retriever = get_hybrid_retriever()
    llm = get_llm()

    # 2. 检索
    docs = retriever.invoke(question)

    print("=" * 50)
    print("检索到文档数量：", len(docs))

    for i, doc in enumerate(docs):
        print(f"\n------ Document {i + 1} ------")
        print(doc.page_content[:300])

    # 3. 拼接 Context
    context = "\n\n".join(doc.page_content for doc in docs)

    print("=" * 50)
    print("Retrieved Context:")
    print(context)
    print("=" * 50)

    # 4. 构造 Prompt
    prompt = RAG_PROMPT.invoke({
        "context": context,
        "question": question
    })

    # 5. 调用 LLM（普通）
    response = llm.invoke(prompt)

    return response.content


# ==========================
# 流式聊天（Streaming）
# ==========================

def rag_chat_stream(question: str):

    retriever = get_hybrid_retriever()
    llm = get_llm(streaming=True)

    docs = retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = RAG_PROMPT.invoke({
        "context": context,
        "question": question
    })


    for chunk in llm.stream(prompt):
        if chunk.content:
            yield f"data: {chunk.content}\n\n"

    # ==========================
    # 简单流式
    # ==========================
    for chunk in llm.stream(prompt):

        if chunk.content:
            yield chunk.content
# ==========================
# 普通 Pipeline
# ==========================
def rag_pipeline(question: str):
    return rag_chat(question)


# ==========================
# Streaming Pipeline
# ==========================
def rag_pipeline_stream(question: str):
    return rag_chat_stream(question)