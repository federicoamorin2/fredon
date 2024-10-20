from typing import Optional

from src.utils import timing_decorator
from src.passage_ import Passages, Passage
from src.event_ import ReRankConfig
from .base import Query, Text
from .model import MonoT5



DEFAULT_MIN_SCORE = -10e10

@timing_decorator
def rerank_prompt(
    query: str,
    passages: Passages,
    rerank_config: ReRankConfig,
    reranker: MonoT5
) -> Passages:
    query = Query(query)
    texts = [Text(passage.text, 0) for passage in passages]
    reranked = reranker.rerank(query, texts)
    top_k_passages = rerank_config.top_k_passages if rerank_config.top_k_passages is not None else len(reranked)
    min_score = rerank_config.min_score if rerank_config.top_k_passages is not None else DEFAULT_MIN_SCORE 
    return Passages(
        [
            Passage(text=passage.text, score=passage.score)
            for passage in reranked[:top_k_passages]
            if passage.score >= min_score
        ]
    )
