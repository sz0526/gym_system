import os
from langchain_community.document_loaders import UnstructuredMarkdownLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# 1. 导入你刚刚在第一步写好的自定义 Embedding
from embedding import LocalServiceEmbeddings

def initialize_vector_store():
    # 初始化你的本地模型服务
    embedding_model = LocalServiceEmbeddings(api_url="http://127.0.0.1:8000/embed")
    
    documents = []
    
    # 2. 读取 Markdown 文件
    md_dir = r"data/fitness_docs"
    if os.path.exists(md_dir):
        for file in os.listdir(md_dir):
            if file.endswith(".md"):
                file_path = os.path.join(md_dir, file)
                print(f"正在加载 Markdown: {file}")
                loader = UnstructuredMarkdownLoader(file_path)
                documents.extend(loader.load())

    # 3. 读取 PDF 文件
    pdf_dir = r"data/pdf"
    if os.path.exists(pdf_dir):
        for file in os.listdir(pdf_dir):
            if file.endswith(".pdf"):
                file_path = os.path.join(pdf_dir, file)
                print(f"正在加载 PDF: {file}")
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())

    if not documents:
        print("未找到任何待处理的 md 或 pdf 文件！")
        return

    print(f"\n文件加载完毕，共读取到 {len(documents)} 个原始文档段落。")

    # 4. 文本切片 (Chunking) 
    # 避免长文本超出模型的最大 Token 限制 (text2vec 通常限制为 512)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,       # 每个切片的最大字符数
        chunk_overlap=50      # 前后切片重叠部分，防止上下文断开
    )
    split_docs = text_splitter.split_documents(documents)
    print(f"文本切片完毕，切分后共有 {len(split_docs)} 个文本块。")

    # 5. 向量化并保存到本地 Chroma 数据库
    print("\n🚀 开始调用本地微服务进行批量 Embedding 并写入数据库...")
    persist_directory = "./chroma_db"
    
    vector_store = Chroma.from_documents(
        documents=split_docs,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    
    print(f"🎉 向量库构建成功！数据已持久化保存至: {persist_directory}")
    return vector_store

if __name__ == "__main__":
    # 确保你的模型服务已经在端口 8000 启动
    initialize_vector_store()