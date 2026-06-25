## Fitness AI Assistant (RAG + Agent) - 智能健身AI助手
基于 SpringBoot + FastAPI + LangChain + LangGraph 构建的智能健身助手。

项目融合 RAG 知识库、Hybrid Retrieval、LangGraph ReAct Agent、Tool Calling 与 MCP 工具服务，实现健身知识问答、课程查询、健身房信息查询、多轮对话记忆及流式 AI 交互。

### 🌟 项目亮点
RAG 知识增强问答：基于 LangChain + Chroma VectorDB 构建健身知识库，实现检索增强生成（RAG），提升专业健身问答准确率。
Hybrid 混合检索：融合 BM25 关键词检索与向量检索，通过 Hybrid Retriever 提升复杂问题召回率与回答准确率。
LangGraph ReAct Agent：基于 LangGraph 构建 Agent 工作流，实现 LLM → Tool → LLM 推理闭环；支持课程查询、健身房信息查询等业务 Tool Calling。
MCP 工具服务：基于 Model Context Protocol（MCP）封装课程查询、健身房信息等业务接口，构建标准 MCP Server，实现工具统一注册与调用。
流式 AI 对话：基于 DashScope Stream API、FastAPI SSE 与 SpringBoot SseEmitter 实现 Token 级流式输出，支持实时对话体验。
多轮上下文记忆：基于 Session 机制维护用户上下文记忆，对话历史持久化至 MySQL，实现跨轮次上下文感知问答与历史追溯。
### 🛠️ 技术栈
<img width="276" height="264" alt="image" src="https://github.com/user-attachments/assets/4d6b657d-8b56-4549-94c7-632b90c5428c" />




### 📁 项目结构
<img width="315" height="291" alt="image" src="https://github.com/user-attachments/assets/2bd195eb-2642-414f-b3c7-0c43bed46841" />







### 🚀 快速开始
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
echo "DASHSCOPE_API_KEY=your_api_key" > .env

# 启动服务
uvicorn app.main:app --reload



### 📡 API 接口
<img width="372" height="202" alt="image" src="https://github.com/user-attachments/assets/f3a20445-7faf-4f6d-ba7a-5995ee4dea1f" />


