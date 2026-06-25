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
<img width="279" height="345" alt="image" src="https://github.com/user-attachments/assets/ea04534e-ed80-4d66-bbf8-f3a75181be78" />
<img width="268" height="275" alt="image" src="https://github.com/user-attachments/assets/00b8327c-c27b-4d21-b436-41b10076c937" />
<img width="276" height="327" alt="image" src="https://github.com/user-attachments/assets/94bfae50-cd6f-4b9e-bc00-535269ac190f" />
<img width="272" height="178" alt="image" src="https://github.com/user-attachments/assets/aea8e125-667f-4bd1-ac7f-195ec4d67e52" />



### 📁 项目结构
```text
gym_system/
├── Fitness-RAG/                    # AI/RAG核心模块
│   ├── app/
│   │   ├── agent.py               # LangGraph Agent工作流
│   │   ├── rag.py                 # RAG主流程（检索+生成）
│   │   ├── retriever.py           # 混合检索策略（向量+BM25）
│   │   ├── reranker.py            # BGE重排序器
│   │   ├── embedding.py           # 文本嵌入生成
│   │   ├── llm.py                 # LLM调用封装
│   │   ├── vector_store.py        # ChromaDB向量存储
│   │   ├── split_text.py          # 文档分块处理
│   │   ├── session.py             # 会话管理
│   │   └── mcp_server.py          # MCP工具服务器
│   ├── chroma_db/                 # 向量数据库存储
│   ├── data/
│   │   ├── fitness_docs/          # 健身知识Markdown文档
│   │   └── pdf/                   # 健身教材PDF
│   └── requirements.txt           # Python依赖
│
├── frontend/                       # Vue3前端
│   ├── src/
│   │   ├── pages/                 # 页面组件
│   │   │   ├── UserChat.vue       # AI聊天页面
│   │   │   ├── UserLogin.vue      # 会员登录
│   │   │   ├── UserRegister.vue   # 会员注册
│   │   │   └── ...                # 其他业务页面
│   │   ├── api/
│   │   │   ├── client.ts          # Axios封装
│   │   │   └── sse.ts             # SSE流式响应
│   │   ├── router/index.ts        # 路由配置
│   │   └── styles/
│   │       └── auth.css           # 认证页面样式
│   └── package.json
│
└── gym-management-system/          # Spring Boot后端
    ├── src/main/java/com/gym/
    │   ├── controller/
    │   │   ├── ApiChatController.java    # AI聊天接口
    │   │   ├── ApiLoginController.java   # 登录注册
    │   │   ├── ApiMemberController.java  # 会员管理
    │   │   ├── ApiClassController.java   # 课程管理
    │   │   └── ...
    │   └── ...
    └── pom.xml

- Node.js 18+
- Java 17+
- MySQL 8.0+

# 设置环境变量
echo "DASHSCOPE_API_KEY=your_api_key" > .env

# 启动服务
# 1. 启动AI服务
cd Fitness-RAG
pip install -r requirements.txt
python main.py

# 2. 启动后端
cd gym-management-system
mvn spring-boot:run

# 3. 启动前端
cd frontend
npm install
npm run dev


