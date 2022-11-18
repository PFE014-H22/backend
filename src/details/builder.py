from operator import itemgetter

from src.details.similarity_score_strategy import SimilarityScoreStrategy


class DetailsBuilder:
    def __init__(self, data: list):
        self.data = data

    def for_keys_list(self, keys_list: list[str]):
        self.keys_list = keys_list
        return self

    def for_parameter_name(self, parameter_name: str):
        self.parameter_name = parameter_name
        return self

    def for_parameter_description(self, parameter_description: str):
        self.parameter_description = parameter_description
        return self

    def with_similarity_score_strategy(self, similarity_score_strategy: SimilarityScoreStrategy):
        self.similarity_score_strategy = similarity_score_strategy
        return self

    def build(self):
        return {
            "parameter": {
                "name": self.parameter_name,
                "description": self.parameter_description,
                "matches": self.get_number_matches()
            },
            "similarity_score": self.get_similarity_score(),
            "sources": self.get_sources(),
        }

    def create_source(self, item: any):
        source = {}
        
        for key in self.keys_list:
            source[key] = item.get(key, None)
        
        return source

    def get_number_matches(self):
        return len(self.data)

    def get_sources(self):
        sources = []

        for item in self.data:
            source = self.create_source(item)
            sources.append(source)

        return sources

    def get_similarity_score(self):
        if self.similarity_score_strategy is SimilarityScoreStrategy.HIGHEST:
            item = max(self.data, key=itemgetter("similarity_score"))
            return item.get("similarity_score")

        if self.similarity_score_strategy is SimilarityScoreStrategy.LOWEST:
            item = min(self.data, key=itemgetter("similarity_score"))
            return item.get("similarity_score")

        if self.similarity_score_strategy is SimilarityScoreStrategy.AVERAGE:
            return sum(data["similarity_score"] for data in self.data) / len(self.data)
