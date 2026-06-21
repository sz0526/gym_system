import os
import faiss
import numpy as np
import dashscope
from dashscope import TextEmbedding

# ==========================================
# 0. API KEY 配置
# ==========================================
# 如果你没有配置系统环境变量，请取消下面这行代码的注释，并填入你的 API Key：
dashscope.api_key = "sk-ws-H.REPYYRY.ICQ8.MEQCID-sKPFo65V8lTraV4sODNbTQzrvwEa0WclMf9glhCtCAiAMkhvscQbqhQee9R4fEi1RHrZ9kVhlP4avpJkkJDt8Gg"

# 定义一个便捷的云端向量化函数
def get_dashscope_embeddings(texts):
    """调用阿里云 DashScope 生成向量，并转换为 FAISS 需要的 float32 格式"""
    response = TextEmbedding.call(
        model=TextEmbedding.Models.text_embedding_v3,
        input=texts
    )
    if response.status_code == 200:
        # 将结果转换为 numpy 数组
        embeddings = np.array([item['embedding'] for item in response.output['embeddings']])
        # 归一化（Normalize），这样后面用 Inner Product (IP) 索引就等价于余弦相似度
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        normalized_embeddings = embeddings / norms
        return normalized_embeddings.astype("float32")
    else:
        raise Exception(f"DashScope 请求失败: {response.code} - {response.message}")


# ==========================================
# 第一步：准备数据（通过云端 API）
# ==========================================
print("【第一步】正在请求 DashScope 生成 10 条文档的向量...")

docs = [
    "如何减肥：科学控制饮食与运动结合",
    "体重管理的有效策略",
    "Python 快速入门教程",
    "深度学习基础与实践",
    "有氧运动对心肺功能的改善",
    "RAG 系统架构设计",
    "向量数据库原理与应用",
    "健康饮食金字塔与营养搭配",
    "Java 并发编程详解",
    "自然语言处理入门",
]

# 核心修改：不再调用本地模型，直接透传云端
embeddings = get_dashscope_embeddings(docs)
dim = embeddings.shape[1]
print(f"-> 向量获取成功！每个向量维度: {dim} (DashScope默认1024), 文档数: {len(docs)}")


# ==========================================
# 第二步：三种索引对比
# ==========================================
print("\n【第二步】准备查询向量，开始索引对比...")
query = "怎么瘦身"
q_vec = get_dashscope_embeddings([query])

# --- Flat：精确暴力 ---
# 特点：一条条死算，最准但数据量大时极慢
index_flat = faiss.IndexFlatIP(dim)   # IP = Inner Product 内积
index_flat.add(embeddings)
D_flat, I_flat = index_flat.search(q_vec, k=3)

print("\n[Flat] 最相似3条：")
for rank, (score, idx) in enumerate(zip(D_flat[0], I_flat[0])):
    print(f"  {rank+1}. ({score:.4f}) {docs[idx]}")

# --- IVF：分簇加速 ---
# 特点：先聚类（分簇），搜的时候只搜离自己最近的几个簇，快但可能漏掉正确答案

nlist = 3   # 聚类成 3 个簇
quantizer = faiss.IndexFlatIP(dim)
index_ivf = faiss.IndexIVFFlat(quantizer, dim, nlist, faiss.METRIC_INNER_PRODUCT)
index_ivf.train(embeddings)   # 倒排索引必须先 train（训练聚类中心）！
index_ivf.add(embeddings)
index_ivf.nprobe = 2          # 查询时搜索离自己最近的 2 个簇

D_ivf, I_ivf = index_ivf.search(q_vec, k=3)
print("\n[IVF nprobe=2] 最相似3条：")
for rank, (score, idx) in enumerate(zip(D_ivf[0], I_ivf[0])):
    print(f"  {rank+1}. ({score:.4f}) {docs[idx]}")

# --- HNSW：图索引 ---
# 特点：构建六度空间一样的“高速路网”，生产环境海量数据检索的绝对主力

index_hnsw = faiss.IndexHNSWFlat(dim, 32)   # 32 = M，每个节点在图里的邻居上限
index_hnsw.add(embeddings)
D_hnsw, I_hnsw = index_hnsw.search(q_vec, k=3)

print("\n[HNSW M=32] 最相似3条：")
for rank, (score, idx) in enumerate(zip(D_hnsw[0], I_hnsw[0])):
    print(f"  {rank+1}. ({score:.4f}) {docs[idx]}")


# ==========================================
# 第三步：持久化索引（生产必用）
# ==========================================
print("\n【第三步】演示持久化...")
# 保存到磁盘（FAISS 索引文件 + 对应的文本列表）
faiss.write_index(index_hnsw, "my_index.faiss")
np.save("my_docs.npy", np.array(docs))
print("-> 索引和文档已成功保存到本地。")

# 模拟：下次程序启动，直接加载，完全不用重新调用 API 费钱费时间
index_loaded = faiss.read_index("my_index.faiss")
docs_loaded = np.load("my_docs.npy", allow_pickle=True).tolist()

D, I = index_loaded.search(q_vec, k=3)
print("\n[加载本地文件后查询] 结果与云端计算一致：")
for score, idx in zip(D[0], I[0]):
    print(f"  ({score:.4f}) {docs_loaded[idx]}")