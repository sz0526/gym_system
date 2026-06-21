import dashscope
from dashscope import TextEmbedding
import numpy as np

dashscope.api_key = "sk-ws-H.REPYYRY.ICQ8.MEQCID-sKPFo65V8lTraV4sODNbTQzrvwEa0WclMf9glhCtCAiAMkhvscQbqhQee9R4fEi1RHrZ9kVhlP4avpJkkJDt8Gg"  # 或设置环境变量 DASHSCOPE_API_KEY

def get_embeddings(texts):
    resp = TextEmbedding.call(
        model=TextEmbedding.Models.text_embedding_v3,
        input=texts
    )
    return np.array([item["embedding"] for item in resp.output["embeddings"]])

def cosine_sim(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

sentences = [
    "我喜欢跑步",
    "我热爱运动",
    "今天天气真好",
    "深度学习很有趣",
]

embeddings = get_embeddings(sentences)
print(f"向量维度: {embeddings.shape}")

query = embeddings[0]
for i, sent in enumerate(sentences[1:], 1):
    sim = cosine_sim(query, embeddings[i])
    print(f"  {sentences[0]} ↔ {sent}: {sim:.4f}")