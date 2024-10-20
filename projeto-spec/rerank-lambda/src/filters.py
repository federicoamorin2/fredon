from typing import List
from dataclasses import dataclass


@dataclass
class Filter:
    name: str


@dataclass
class Filters:
    filter_list: List[Filter]

    @classmethod
    def from_raw(cls, filters):
        return cls(
            [Filter(**filter_) for filter_ in filters]
        )
