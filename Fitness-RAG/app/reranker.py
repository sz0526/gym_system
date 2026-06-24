"""
BGE Reranker 重排序模块
- 对初步召回结果进行语义二次排序
- 提供排序效果评估指标
"""
from typing import List, Tuple, Optional
from sentence_transformers import CrossEncoder
import numpy as np


class BGEReranker:
    """BGE Cross-Encoder 重排序器"""

    def __init__(self, model_name: str = "BAAI/bge-reranker-v2-m3", local_model_path: Optional[str] = None):
        self.model_name = model_name
        self.local_model_path = local_model_path
        self.model: Optional[CrossEncoder] = None

    def _load_model(self):
        if self.model is None:
            model_path = self.local_model_path if self.local_model_path else self.model_name
            self.model = CrossEncoder(
                model_path,
                max_length=512,
                device="cpu",
                local_files_only=True if self.local_model_path else False
            )
        return self.model

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 3
    ) -> List[Tuple[int, float, str]]:
        """
        对文档列表进行重排序
        返回: [(原始索引, 相关度分数, 文档内容), ...] 按分数降序排列
        """
        if not documents:
            return []

        model = self._load_model()
        pairs = [[query, doc] for doc in documents]
        scores = model.predict(pairs, show_progress_bar=False)

        ranked = sorted(
            enumerate(zip(scores, documents)),
            key=lambda x: x[1][0],
            reverse=True
        )
        ranked = ranked[:top_k]

        return [(idx, score, doc) for idx, (score, doc) in ranked]


def evaluate_retrieval(
    query: str,
    retrieved_docs: List[str],
    relevant_doc_indices: List[int],
    top_k: int = 3
) -> dict:
    """
    评估检索效果指标
    :param query: 查询文本
    :param retrieved_docs: 检索到的文档列表
    :param relevant_doc_indices: 标注的相关文档索引列表
    :param top_k: 取前K个结果评估
    :return: {"precision": float, "recall": float, "f1": float}
    """
    if not retrieved_docs or not relevant_doc_indices:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    top_k = min(top_k, len(retrieved_docs))
    top_indices = set(range(top_k))

    relevant_set = set(relevant_doc_indices)
    retrieved_top_set = top_indices

    hit_count = len(relevant_set & retrieved_top_set)

    precision = hit_count / top_k if top_k > 0 else 0.0
    recall = hit_count / len(relevant_set) if relevant_set else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4)
    }