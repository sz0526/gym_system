## Fitness-RAG - 智能健身AI助手
基于检索增强生成（RAG）技术的智能健身AI助手，为用户提供专业、准确的健身指导。

### 🌟 项目亮点
- 检索增强生成 ：结合向量数据库与大语言模型，确保回答精准、有据可依
- 混合检索策略 ：融合关键词检索（BM25）与向量检索，提升召回率
- 流式响应 ：支持SSE流式输出，实现实时对话体验
- 专业健身知识库 ：内置《现代抗阻训练基础教材》等专业健身资料
- 易于扩展 ：模块化设计，支持新增知识文档
### 🛠️ 技术栈
<img width="276" height="264" alt="image" src="https://github.com/user-attachments/assets/4d6b657d-8b56-4549-94c7-632b90c5428c" />
### 📁 项目结构
Fitness-RAG/
├── app/                    # 核心应用代码
│   ├── main.py             # FastAPI 入口
│   ├── rag.py              # RAG 核心逻辑
│   ├── retriever.py        # 混合检索器
│   ├── vector_store.py     # 向量数据库管理
│   ├── embedding.py        # 向量化模型
│   ├── llm.py              # LLM 客户端
│   ├── llm_stream.py       # 流式 LLM 客户端
│   ├── prompt.py           # Prompt 模板
│   ├── load_markdown.py    # 文档加载器
│   ├── split_text.py       # 文本切分工具
│   └── config.py           # 配置管理
├── data/                   # 数据目录
│   ├── fitness_docs/       # 健身知识库文档
│   └── pdf/                # PDF 文档
├── chroma_db/              # Chroma 向量数据库存储
├── .env                    # 环境变量配置
├── requirements.txt        # 依赖清单
└── README.md               # 项目说明
### 🚀 快速开始
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
echo "DASHSCOPE_API_KEY=your_api_key" > .env

# 启动服务
uvicorn app.main:app --reload

# 访问 API
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "怎么练胸肌？"}'
### 📡 API 接口
<img width="277" height="100" alt="image" src="https://github.com/user-attachments/assets/baa97012-3ce8-4d57-9874-34be530c82cc" />

