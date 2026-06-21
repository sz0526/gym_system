from langchain_chroma import Chroma
from app.embedding import LocalServiceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

def get_base_vector_store():
    """基础函数：连接本地已有的 Chroma 数据库"""
    
    embedding_model = LocalServiceEmbeddings()
    return Chroma(
        persist_directory="./chroma_db", 
        embedding_function=embedding_model
    )

# ==================== 1. Similarity 检索器 ====================
def get_similarity_retriever(k: int = 3):
    """
    基础相似度检索器
    :param k: 最终返回给大模型的文本块数量
    """
    db = get_base_vector_store()
    # search_type="similarity" 是 LangChain 的默认检索方式
    return db.as_retriever(
        search_type="similarity", 
        search_kwargs={"k": k}
    )

# ==================== 2. MMR 检索器 ====================
def get_mmr_retriever(k: int = 3, fetch_k: int = 10):
    """
    最大边际收益检索器（兼顾相关性与多样性，防冗余）
    :param k: 最终返回给大模型的文本块数量
    :param fetch_k: 算法第一步在库里盲捞出的候选块数量（必须大于 k）
    """
    db = get_base_vector_store()
    return db.as_retriever(
        search_type="mmr", 
        search_kwargs={
            "k": k, 
            "fetch_k": fetch_k,
            "lambda_mult": 0.5  # 0代表完全多样，1代表纯相似度。0.5是黄金平衡点
        }
    )

# ==================== 3. Hybrid 混合检索器 ====================
def get_hybrid_retriever(k: int = 3):
    """
    企业级混合检索器：50% 关键词检索 (BM25) + 50% 向量检索 (Chroma)
    """
    db = get_base_vector_store()
    
    # 路 A：向量检索器
    vector_retriever = db.as_retriever(search_kwargs={"k": k})
    
    # 路 B：关键词检索器（需要从现有的数据库里抽出所有的文本来建立关键词树）
    db_data = db.get()
    all_texts = db_data.get("documents", [])
    all_metadatas = db_data.get("metadatas", [])
    
    if not all_texts:
        raise Exception("❌ 数据库是空的，请先运行 vector_store.py 导入数据！")
        
    # 把文本包装成 LangChain 的 Document 格式
    from langchain_core.documents import Document
    docs = [
        Document(page_content=t, metadata=m) 
        for t, m in zip(all_texts, all_metadatas)
    ]
    
    bm25_retriever = BM25Retriever.from_documents(docs)
    bm25_retriever.k = k  # 设置关键词检索也返回 k 个
    
    # 合并两路：使用 EnsembleRetriever
    hybrid_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[0.5, 0.5]  # 权重平分
    )
    return hybrid_retriever

# ==================== 本章实战测试入口 ====================
if __name__ == "__main__":
    print("🤖 开始 Retriever 策略测试...")
    
    test_query = "胸肌怎么练？"
    
    # ==================== 测试一：Similarity 检索器 ====================
    print(f"\n--- 🎯 1. 正在使用 Similarity (基础相似度) 检索器查询: 【{test_query}】 ---")
    try:
        similarity_retriever = get_similarity_retriever(k=2)
        sim_docs = similarity_retriever.invoke(test_query)
        
        for i, doc in enumerate(sim_docs):
            print(f"片段 {i+1} [来自: {doc.metadata.get('source', '未知')}]:")
            print(f"内容: {doc.page_content[:100]}...\n")
    except Exception as e:
        print(f"Similarity 检索失败: {e}")

    # ==================== 测试二：MMR 检索器 ====================
    print(f"\n--- ⚡ 2. 正在使用 MMR (去重多样性) 检索器查询: 【{test_query}】 ---")
    try:
        mmr_retriever = get_mmr_retriever(k=2)
        mmr_docs = mmr_retriever.invoke(test_query)
        
        for i, doc in enumerate(mmr_docs):
            print(f"片段 {i+1} [来自: {doc.metadata.get('source', '未知')}]:")
            print(f"内容: {doc.page_content[:100]}...\n")
    except Exception as e:
        print(f"MMR 检索失败: {e}")

    # ==================== 测试三：Hybrid 混合检索器 ====================
    print(f"\n--- 🔀 3. 正在使用 Hybrid (混合检索) 检索器查询: 【{test_query}】 ---")
    try:
        hybrid_retriever = get_hybrid_retriever(k=2)
        hybrid_docs = hybrid_retriever.invoke(test_query)
        
        for i, doc in enumerate(hybrid_docs):
            print(f"片段 {i+1} [来自: {doc.metadata.get('source', '未知')}]:")
            print(f"内容: {doc.page_content[:100]}...\n")
    except Exception as e:
        print(f"Hybrid 检索失败: {e}")