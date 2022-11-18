from operator import itemgetter

from src.details.similarity_score_strategy import SimilarityScoreStrategy


class DetailsBuilder:
    def __init__(self, data: list):
        self.data = data

    def for_parameter(self, parameter: str):
        self.parameter = parameter
        return self

    def for_parameter_description(self, parameter_description: str):
        self.parameter_description = parameter_description
        return self

    def with_similarity_score_strategy(self, strategy: SimilarityScoreStrategy):
        self.similarity_score_strategy = strategy
        return self

    def build(self):
        return {
            "parameter": {
                "name": self.parameter,
                "description": self.parameter_description,
                "matches": self.get_number_matches()
            },
            "similarity_score": self.get_similarity_score(),
            "sources": self.get_sources(),
        }

    def create_source(self, item: any):
        source = {}
        source["answer_id"] = item.get("answer_id", -1)
        source["is_accepted"] = item.get("is_accepted", False)
        source["link"] = item.get("link", "")
        source["name"] = item.get("name", "")
        source["question_body"] = item.get("question_body", "")
        source["question_id"] = item.get("question_id", "")
        source["question_title"] = item.get("question_title", "")
        source["response_body"] = item.get("response_body", "")
        source["similarity_score"] = item.get("similarity_score", -1)
        source["tags"] = item.get("tags", [])
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
