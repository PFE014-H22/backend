from operator import itemgetter
from typing import List

from src.details.similarity_score_strategy import SimilarityScoreStrategy


class DetailsBuilder:
    def __init__(self,  data: list, parameter_name: str, parameter_description: str, similarity_score_strategy: SimilarityScoreStrategy, keys_list: List[str]):
        self.data = data
        self.parameter_name = parameter_name
        self.parameter_description = parameter_description
        self.similarity_score_strategy = similarity_score_strategy
        self.keys_list = keys_list

    def build(self):
        return {
            "parameter": {
                "name": self.parameter_name,
                "description": self.parameter_description,
                "matches": self._get_number_matches()
            },
            "similarity_score": self._get_similarity_score(),
            "sources": self._get_sources(),
        }

    def _create_source(self, item: any):
        source = {}

        for key in self.keys_list:
            source[key] = item.get(key, None)

        return source

    def _get_number_matches(self):
        return len(self.data)

    def _get_sources(self):
        sources = []

        for item in self.data:
            source = self._create_source(item)
            sources.append(source)

        return sources

    def _get_similarity_score(self):
        if self.similarity_score_strategy is SimilarityScoreStrategy.HIGHEST:
            item = max(self.data, key=itemgetter("similarity_score"))
            return item.get("similarity_score")

        if self.similarity_score_strategy is SimilarityScoreStrategy.LOWEST:
            item = min(self.data, key=itemgetter("similarity_score"))
            return item.get("similarity_score")

        if self.similarity_score_strategy is SimilarityScoreStrategy.AVERAGE:
            return sum(data["similarity_score"] for data in self.data) / len(self.data)
