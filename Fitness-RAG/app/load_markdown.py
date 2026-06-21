import os
import pickle
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader

# 1. 定义文件夹路径和输出路径
docs_dir = "data/fitness_docs"
output_data_path = "data/loaded_docs.pkl"

# 确保保存数据的目录存在
os.makedirs(os.path.dirname(output_data_path), exist_ok=True)

print(f"正在一次性读取文件夹下所有 Markdown 文档: {docs_dir} ...")

# 2. 使用 DirectoryLoader 批量读取该目录下所有以 .md 结尾的文件
loader = DirectoryLoader(
    docs_dir, 
    glob="*.md", 
    loader_cls=UnstructuredMarkdownLoader
)
docs = loader.load()

print("真实Document数量:", len(docs))

for i, doc in enumerate(docs):
    print("=" * 40)
    print("DOC:", i)
    print("source:", doc.metadata.get("source"))
    print("content前100字符:", doc.page_content[:100])

print("=" * 50)
print(f"所有文档读取成功！一共读取了 {len(docs)} 个原始文档。")

# 打印一下读取到了哪些文件，方便你确认
for i, doc in enumerate(docs):
    source_file = doc.metadata.get('source', '未知文件')
    print(f"  文档 {i+1}: {source_file}")
print("=" * 50)

# 3. 将所有文档对象打包保存到本地
with open(output_data_path, "wb") as f:
    pickle.dump(docs, f)

print(f"已将所有文档数据保存至: {output_data_path}，请运行 split_text.py 进行批量切块。")