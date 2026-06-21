import chromadb
import dashscope
import streamlit
import fastapi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

print("Python 环境正常")
print("Chroma:", chromadb.__version__)
print("DashScope: OK")
print("FastAPI:", fastapi.__version__)
print("Streamlit:", streamlit.__version__)
print("LangChain 文本切分器加载成功:", RecursiveCharacterTextSplitter)
print("PyPDFLoader 加载成功:", PyPDFLoader)