import os
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from embedding import LocalServiceEmbeddings

def update_file_in_chroma(file_path: str):
    """
    企业级 RAG 向量库更新标准流：先删后增
    :param file_path: 需要更新的文件路径，例如 'data/fitness_docs\胸肌训练.md'
    """
    embedding_model = LocalServiceEmbeddings()
    vector_store = Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)
    
    # ==================== 第一步：删 (你刚才已经做过的操作) ====================
    print(f"\n🔄 开始更新流程：正在检查库中是否存在旧的 {file_path}...")
    db_data = vector_store.get(where={"source": file_path})
    ids_to_delete = db_data.get("ids", [])
    
    if ids_to_delete:
        print(f"🗑️ 发现旧向量片段 {len(ids_to_delete)} 个，正在执行清理...")
        vector_store.delete(ids=ids_to_delete)
        print("✅ 旧向量清理完毕。")
    else:
        print("💡 库中未发现该文件的旧向量，将直接作为新文件导入。")

    # ==================== 第二步：增 (读取新内容并重新写入) ====================
    if not os.path.exists(file_path):
        print(f"❌ 错误：本地未找到文件 {file_path}，请确认文件路径是否正确！")
        return

    print(f"📖 正在读取最新的文件内容: {file_path}")
    
    # 1. 纯 Python 读取最新文本
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 2. 包装成 LangChain 认识的 Document 对象（必须带上元数据 source，方便下次还能删）
    new_doc = Document(page_content=content, metadata={"source": file_path})
    
    # 3. 重新切片 (Chunking) — 对应你的第四章知识
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    split_docs = text_splitter.split_documents([new_doc])
    print(f"✂️ 重新切片成功，切分为 {len(split_docs)} 个最新文本块。")
    
    # 4. 重新向量化并存入 Chroma — 对应你的第五、六章知识
    print("🚀 正在调用本地微服务生成最新向量并写入库中...")
    vector_store.add_documents(documents=split_docs)
    print(f"🎉 文件 {file_path} 已成功更新到 Chroma 向量数据库！")

if __name__ == "__main__":
    # 【测试更新】
    # 比如你修改了本地的 "data/fitness_docs\胸肌训练.md" 的内容
    # 运行这行代码，库里该文件的向量就会瞬间变成最新的
    target_file = "data/fitness_docs\胸肌训练.md"
    update_file_in_chroma(target_file)