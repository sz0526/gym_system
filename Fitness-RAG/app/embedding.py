import requests
from typing import List

class LocalServiceEmbeddings:
    """自定义 Embedding 类，对接本地跑的 text2vec 微服务"""
    def __init__(self, api_url: str = "http://127.0.0.1:8000/embed"):
        self.api_url = api_url

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """为文档列表生成向量"""
        if not texts:
            return []
        try:
            response = requests.post(self.api_url, json={"texts": texts}, timeout=30)
            if response.status_code == 200:
                return response.json()["embeddings"]
            else:
                raise Exception(f"模型服务返回错误: {response.text}")
        except Exception as e:
            print(f"Embedding 失败: {e}")
            raise e

    def embed_query(self, text: str) -> List[float]:
        """为用户的单个提问生成向量"""
        return self.embed_documents([text])[0]