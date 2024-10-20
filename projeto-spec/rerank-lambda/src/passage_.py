from typing import List
from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Passage:
    score: float
    text: str
    id: str = field(default=str(uuid4()))


@dataclass
class Passages:
    passage_list: List[Passage]

    def filter_by_score(self, min_score: float) -> 'Passages':
        print(self.passage_list[0])
        return Passages(
            [passage for passage in self.passage_list if passage.score >= min_score]
        )

    def build_prompt(self):
        return "\n\n".join([passage.text for passage in self.passage_list])

    def __len__(self):
        return len(self.passage_list)

    def __iter__(self):
        return iter(self.passage_list)