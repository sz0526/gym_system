## Fitness AI Assistant (RAG + Agent) - 智能健身AI助手
基于 SpringBoot + FastAPI + LangChain + LangGraph 构建的智能健身助手。

项目融合 RAG 知识库、Hybrid Retrieval、LangGraph ReAct Agent、Tool Calling 与 MCP 工具服务，实现健身知识问答、课程查询、健身房信息查询、多轮对话记忆及流式 AI 交互。


### 📊 架构关系图
================================================================================
                    gym_system 综合健身管理系统 (总根目录)
================================================================================
                               |
        +----------------------+----------------------+
        |                      |                      |
        v                      v                      v
+---------------+      +---------------+      +------------------------+
|  Fitness-RAG  |      |   frontend    |      | gym-management-system  |
| (AI/RAG核心模块) |      |  (Vue3前端)   |      |   (Spring Boot后端)    |
+-------+-------+      +-------+-------+      +-----------+------------+
        |                      |                          |
        |-- app/ (工作流/RAG)   |-- src/pages/ (业务页面)   |-- controller/ (API层)
        |-- chroma_db/ (向量库) |-- src/api/ (接口/SSE)    |-- service/ (业务逻辑)
        |-- data/ (Markdown库) |-- src/router/ (双套路由)  |-- mapper/ & pojo/ (数据)
        |                                                 |-- security/ (认证拦截)
        |                                                             |
        +---------------------> [ MySQL 8.0 数据库 ] <----------------+
                       (共享业务数据 / 存储持久化 AI 会话消息)

--------------------------------------------------------------------------------
【系统核心数据链路】
  [前端 Vue3 页面] --(HTTP/SSE流式交互)--> [后端 Spring Boot] --(内部调用)--> [Fitness-RAG服务]
================================================================================




### 🌟 项目亮点
RAG 知识增强问答：基于 LangChain + Chroma VectorDB 构建健身知识库，实现检索增强生成（RAG），提升专业健身问答准确率。

Hybrid 混合检索：融合 BM25 关键词检索与向量检索，通过 Hybrid Retriever 提升复杂问题召回率与回答准确率。

LangGraph ReAct Agent：基于 LangGraph 构建 Agent 工作流，实现 LLM → Tool → LLM 推理闭环；支持课程查询、健身房信息查询等业务 Tool Calling。

MCP 工具服务：基于 Model Context Protocol（MCP）封装课程查询、健身房信息等业务接口，构建标准 MCP Server，实现工具统一注册与调用。

流式 AI 对话：基于 DashScope Stream API、FastAPI SSE 与 SpringBoot SseEmitter 实现 Token 级流式输出，支持实时对话体验。

多轮上下文记忆：基于 Session 机制维护用户上下文记忆，对话历史持久化至 MySQL，实现跨轮次上下文感知问答与历史追溯。


### 🛠️ 技术栈
# AI/RAG
| 技术 | 版本 | 用途 |
| :--- | :---: | :--- |
| **Python** | 3.x | AI服务开发语言 |
| **LangChain** | 0.2.x | RAG框架，构建检索增强生成流程 |
| **LangChain Core** | 0.2.x | LangChain核心模块 |
| **LangChain Community** | 0.2.x | 社区集成模块（BM25等） |
| **LangChain Chroma** | 0.1.x | ChromaDB向量数据库集成 |
| **LangChain OpenAI** | 0.1.x | OpenAI兼容API集成（调用通义千问） |
| **LangChain HuggingFace** | 0.0.x | HuggingFace模型集成 |
| **LangGraph** | 1.2.x | Agent工作流编排，支持多工具调用 |
| **LangGraph Prebuilt** | 1.1.x | LangGraph预构建节点 |
| **ChromaDB** | 0.5.23 | 向量数据库，存储健身知识文档嵌入 |
| **BGE Reranker** | - | 重排序模型（BAAI/bge-reranker-v2-m3） |
| **Sentence Transformers** | 5.5.x | 文本嵌入生成模型 |
| **阿里云通义千问** | qwen-plus | 大语言模型，生成专业健身建议 |
| **BM25** | rank-bm25 | 关键词检索，混合检索策略之一 |
| **FastAPI** | 0.137.x | AI服务HTTP接口 |
| **Uvicorn** | 0.49.x | ASGI服务器 |
| **Streamlit** | 1.58.x | 可视化演示界面 |
| **NumPy** | 1.26.x | 数值计算 |
| **Pandas** | 3.0.x | 数据处理 |
| **PyTorch** | 2.11.x | 深度学习框架 |
| **Transformers** | 5.6.x | HuggingFace模型加载 |


# 前端
| 技术 | 版本 | 用途 |
| :--- | :---: | :--- |
| **Vue** | 3.5.30 | 渐进式前端框架 |
| **TypeScript** | 5.9.3 | 类型安全开发 |
| **Vite** | 8.0.1 | 构建工具，开发服务器 |
| **Element Plus** | 2.13.6 | UI组件库 |
| **@element-plus/icons-vue** | 2.3.2 | Element Plus图标库 |
| **Vue Router** | 5.0.4 | 路由管理 |
| **Axios** | 1.14.0 | HTTP客户端 |
| **@vitejs/plugin-vue** | 6.0.5 | Vue Vite插件 |
| **ESBuild** | 0.28.1 | JavaScript/TypeScript编译器 |


# 后端
| 技术 | 版本 | 用途 |
| :--- | :---: | :--- |
| **Java** | 17 | 后端开发语言 |
| **Spring Boot** | 3.2.5 | Java后端框架 |
| **Spring Web** | - | Web MVC支持 |
| **MyBatis** | 3.0.4 | ORM持久层框架 |
| **MyBatis Spring Boot Starter** | 3.0.4 | MyBatis与Spring Boot集成 |
| **MySQL Connector** | 8.0.33 | MySQL数据库驱动 |
| **Lombok** | - | Java代码简化（注解处理器） |
| **Jakarta Servlet** | - | Servlet API |


# 数据库、通信协议、开发工具与部署环境
| 分类 | 技术/工具 | 版本/说明 | 用途 |
| :--- | :--- | :---: | :--- |
| **数据库** | **MySQL** | 8.0.33 | 关系型数据库，存储业务数据（会员、课程、设备等） |
| **数据库** | **SQLite** | - | ChromaDB内置数据库，存储向量索引元数据 |
| **数据库** | **ChromaDB HNSW** | 0.7.x | 向量索引算法（Hierarchical Navigable Small Worlds） |
| **通信协议** | **HTTP/HTTPS** | - | 主要API通信 |
| **通信协议** | **SSE (Server-Sent Events)** | - | AI流式响应推送 |
| **通信协议** | **WebSocket** | - | 实时通信 |
| **通信协议** | **MCP (Model Context Protocol)** | - | AI工具调用协议 |
| **通信协议** | **CORS** | - | 跨域资源共享 |
| **开发工具** | **Maven** | - | Java项目构建管理 |
| **开发工具** | **npm** | - | Node.js包管理 |
| **开发工具** | **Git** | - | 版本控制 |
| **开发工具** | **Visual Studio Code** | - | 集成开发环境（IDE） |
| **运行环境** | **Windows** | - | 开发运行环境 |
| **运行环境** | **Tomcat** | - | Spring Boot内置Web服务器 |
| **运行环境** | **Vite Dev Server** | 端口 5173 | 前端开发服务器 |
| **运行环境** | **Spring Boot Server** | 端口 8080 | 后端内嵌服务器部署 |

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


## 环境要求
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


