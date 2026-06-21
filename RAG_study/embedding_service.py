import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from typing import List

# 1. 初始化 FastAPI 应用
app = FastAPI(
    title="Text2Vec 向量化服务", 
    description="供其他项目调用的本地 Embedding 微服务"
)

# 2. 加载本地模型（服务启动时仅加载一次，常驻内存）
MODEL_PATH = r"D:\RAG_study\text2vec_model"
print("正在加载本地 text2vec 模型，请稍候...")
try:
    model = SentenceTransformer(MODEL_PATH)
    print("模型加载成功！服务准备就绪。")
except Exception as e:
    print(f"模型加载失败，请检查路径是否正确。错误信息: {e}")
    raise e

# 3. 定义请求体的数据格式（支持单条文本或批量文本）
class EmbeddingRequest(BaseModel):
    texts: List[str]  # 接收一个字符串列表，例如 ["你好", "世界"]

# 4. 编写核心的 API 路由
@app.post("/embed")
def get_embeddings(request: EmbeddingRequest):
    if not request.texts:
        raise HTTPException(status_code=400, detail="文本列表不能为空")
    
    try:
        # 使用模型提取向量，并将其转换为标准的 Python 列表（List[List[float]]）
        embeddings = model.encode(request.texts)
        embeddings_list = embeddings.tolist()
        
        return {
            "success": True,
            "embeddings": embeddings_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"向量化计算失败: {str(e)}")

# 5. 允许直接运行该脚本启动服务
if __name__ == "__main__":
    # 启动在本地 8000 端口
    uvicorn.run("embedding_service:app", host="127.0.0.1", port=8000, reload=False)