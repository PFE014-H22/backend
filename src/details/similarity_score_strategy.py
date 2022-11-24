from enum import Enum


class SimilarityScoreStrategy(Enum):
    """
    Enum for algorithm for the similarity score for the aggregated parameter.
    """

    HIGHEST = 1
    """
    Use the highest similarity score.
    """
 
    LOWEST = 2
    """
    Use the lowest similarity score.
    """
  
    AVERAGE = 3
    """
    Use the average of the similarity scores.
    """