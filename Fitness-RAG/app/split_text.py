from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. 批量加载
loader = DirectoryLoader(
    "data/fitness_docs",
    glob="*.md",
    loader_cls=UnstructuredMarkdownLoader
)

docs = loader.load()

print("原始Document数量：", len(docs))

# 2. 切块
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_documents(docs)

print("切块后数量：", len(chunks))