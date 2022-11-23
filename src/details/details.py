from operator import itemgetter
from typing import List

from src.details.similarity_score_strategy import SimilarityScoreStrategy


class Details:
    """
    This class represents the details for a configuration parameter.
    """

    def __init__(self,  data: List[dict], parameter_name: str, parameter_description: str, similarity_score_strategy: SimilarityScoreStrategy, keys_list: List[str]):
        self.data = data
        self.parameter_name = parameter_name
        self.parameter_description = parameter_description
        self.similarity_score_strategy = similarity_score_strategy
        self.keys_list = keys_list

    def to_json(self):
        """
        Returns a JSON representation of the details object.
        """

        return {
            "parameter": {
                "name": self.parameter_name,
                "description": self.parameter_description,
                "matches": self._get_number_matches()
            },
            "similarity_score": self._get_similarity_score(),
            "sources": self._get_sources(),
        }

    def _create_source(self, item: dict):
        """
        Utility function that creates the source object dictionary with the keys list.
        """

        source = {}

        for key in self.keys_list:
            source[key] = item.get(key, None)

        return source

    def _get_number_matches(self):
        """
        Utility function that returns the number of matches for each configuration parameters.
        """

        return len(self.data)

    def _get_sources(self):
        """
        Utility function that returns a list of source objects for each configuration parameters.
        """

        sources = []

        for item in self.data:
            source = self._create_source(item)
            sources.append(source)

        return sources

    def _get_similarity_score(self):
        """
        Utility function that returns the similarity score for each configuration parameters based on the similarity score strategy.
        """

        if self.similarity_score_strategy is SimilarityScoreStrategy.HIGHEST:
            item = max(self.data, key=itemgetter("similarity_score"))
            return item.get("similarity_score")

        if self.similarity_score_strategy is SimilarityScoreStrategy.LOWEST:
            item = min(self.data, key=itemgetter("similarity_score"))
            return item.get("similarity_score")

        if self.similarity_score_strategy is SimilarityScoreStrategy.AVERAGE:
            return sum(data["similarity_score"] for data in self.data) / len(self.data)
