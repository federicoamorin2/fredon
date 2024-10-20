from typing import Any, Dict, Optional, List
from dataclasses import dataclass
from uuid import uuid4

from .filters import Filters

Event = Dict[str, Any]

@dataclass
class ReRankConfig:
    top_k_passages: Optional[int]
    min_score: Optional[float]
    
    @classmethod
    def from_raw(cls, raw):
        return cls(
            top_k_passages=raw.get("kTopPassages"),
            min_score=raw.get("minScore")
        )


@dataclass
class RagEvent:
    query: str
    index: str
    filters: Optional[Filters]
    top_k_passages: int
    rerank_config: Optional[ReRankConfig]
    min_score: float
    adjacent_passages: int

    @classmethod
    def from_event(cls, event: Event):
        return cls(
            query=event["query"],
            index=event["index"],
            filters=cls.__optional_parsing(event, "filters", Filters),
            top_k_passages=int(event.get("kTopPassages", 5)),
            rerank_config=cls.__optional_parsing(event, "reRankConfig", ReRankConfig),
            min_score=float(event.get("minScore", 0)),
            adjacent_passages=int(event.get("adjacentPassages", 0))
        )
    
    @staticmethod
    def __optional_parsing(event: Event, attribute: str, parsing_class: Any):
        if (attr_val := event.get(attribute)) is None:
            return None
        return parsing_class.from_raw(attr_val) 

    @property
    def has_rerank(self):
        return self.rerank_config is not None 

    @property
    def has_min_score(self):
        return self.min_score != 0

    @property 
    def has_get_adjacent_passages(self):
        return bool(self.adjacent_passages)
