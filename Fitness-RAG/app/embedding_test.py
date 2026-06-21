from langchain_chroma import Chroma
from embedding import LocalServiceEmbeddings

vector_store = Chroma(persist_directory="./chroma_db", embedding_function=LocalServiceEmbeddings())

# 1. 把库里所有数据的元数据（Metadata）全捞出来
all_data = vector_store.get()
metadatas = all_data.get("metadatas", [])

# 2. 用 Python 的集合（Set）去重，看看都有哪些文件在库里
existing_files = set([meta.get("source") for meta in metadatas if meta])

print("当前 Chroma 数据库中真正存在的文件路径有：")
for file in existing_files:
    print(f"📍 {file}")