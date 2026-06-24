## Fitness-RAG - 智能健身AI助手
基于检索增强生成（RAG）技术的智能健身AI助手，为用户提供专业、准确的健身指导。

### 🌟 项目亮点
- 检索增强生成 ：结合向量数据库与大语言模型，确保回答精准、有据可依
- 混合检索策略 ：融合关键词检索（BM25）与向量检索，提升召回率
- 流式响应 ：支持SSE流式输出，实现实时对话体验
- 多轮上下文记忆：基于会话管理实现多轮对话，AI 可理解上下文连续追问
- 专业健身知识库 ：内置《现代抗阻训练基础教材》等专业健身资料
- 易于扩展 ：模块化设计，支持新增知识文档
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


