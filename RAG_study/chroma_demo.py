import os
import chromadb
from chromadb.utils.embedding_functions import EmbeddingFunction
from sentence_transformers import SentenceTransformer

# ==========================================
# 1. 自定义本地 HuggingFace 嵌入组件
# ==========================================
class LocalEmbeddingFunction(EmbeddingFunction):
    """让 ChromaDB 自动调用你下载到本地的 text2vec 模型"""
    def __init__(self, model_path):
        print(f"正在从本地路径加载模型: {model_path} ...")
        # 直接加载本地硬盘上的权重，完全不需要联网
        self.model = SentenceTransformer(model_path)
        print("本地模型加载成功！")

    def __call__(self, input_texts):
        # 获得稠密向量，并转化为 ChromaDB 要求的 List[List[float]] 格式
        embeddings = self.model.encode(input_texts, normalize_embeddings=True)
        return embeddings.tolist()

# ==========================================
# 2. 初始化持久化数据库
# ==========================================
# 数据会真实写到本地的 D:\RAG_study\my_chroma_db 文件夹中，下次启动直接读取
client = chromadb.PersistentClient(path="./my_chroma_db")

# 核心修改：指定本地绝对路径
LOCAL_MODEL_PATH = "D:/RAG_study/text2vec_model"
local_ef = LocalEmbeddingFunction(LOCAL_MODEL_PATH)

# 创建或获取一个“集合”(Collection)，类似于关系型数据库的“表”
# 显式指定使用余弦相似度 (cosine) 作为距离量度
collection = client.get_or_create_collection(
    name="my_knowledge_base", 
    embedding_function=local_ef,
    metadata={"hnsw:space": "cosine"} 
)

# ==========================================
# 3. 技能核心：C (Create) - 写入文档、元数据与ID
# ==========================================
print("\n【Create】正在向本地 ChromaDB 写入文档与元数据标签...")

# 模拟我们有一堆不同类别、不同年份的本地知识库文档
documents_data = [
    "Python 异步编程与高并发架构指南", 
    "2026年最新款人工智能手机发布调研报告", 
    "健康轻食：如何科学搭配每日膳食营养"
]

collection.add(
    documents=documents_data,
    metadatas=[
        {"category": "tech", "year": 2026},
        {"category": "tech", "year": 2026},
        {"category": "health", "year": 2025}
    ],
    ids=["doc_001", "doc_002", "doc_003"]
)
print("-> 3条文档已全部打散、生成向量，并安全存入本地 HNSW 结构中。")

# ==========================================
# 4. 技能核心：R (Read) - 语义搜索 + 元数据条件过滤
# ==========================================
print("\n【Read】正在执行高级语义搜索（带有元数据硬过滤）...")

# 搜索意图包含“技术”，但我们强制添加 where 条件：只在 category 为 tech 的数据里搜
results = collection.query(
    query_texts=["推荐一些编程或者硬件教程"], 
    n_results=2,
    where={"category": "tech"} # 🌟 元数据过滤核心句
)

print("-> 过滤搜索结果：")
for doc, score, meta in zip(results['documents'][0], results['distances'][0], results['metadatas'][0]):
    # 注意：ChromaDB 在余弦空间下返回的距离是 (1 - CosSim)。
    # 距离越接近 0，说明它们在语义空间里越相似！
    print(f"  [语义距离: {score:.4f}] 内容: {doc} | 标签: {meta}")

# ==========================================
# 5. 技能核心：U (Update) & D (Delete)
# ==========================================
print("\n【Update & Delete】正在维护本地数据...")

# U: 覆盖更新 doc_001 的文本内容
collection.update(
    ids=["doc_001"],
    documents=["Python 异步编程高级进阶：从原理到企业级微服务部署框架"]
)
print("-> doc_001 内容更新完毕。")

# D: 从向量数据库中彻底销毁 doc_003 (健康轻食)
collection.delete(ids=["doc_003"])
print("-> doc_003 已从 HNSW 树中移除。")