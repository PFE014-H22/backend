from typing import List


class DetailsAggregator:
    """
    Aggregation class that groups objects based on values of a specific key.
    """

    def __init__(self, data: List[dict], aggregation_key: str):
        self.data = data
        self.aggregation_key = aggregation_key

    def aggregate(self):
        """
        Iterates through the data and aggregates the objects by key.
        """

        aggregation_dict = {}

        for data in self.data:
            if self.aggregation_key in data.keys():
                current_key = data.get(self.aggregation_key)

                # If the key for the current aggregation key is an array
                if type(current_key) is list:
                    self._aggregate_list_with_key(data, aggregation_dict, current_key)
                else:
                    self._aggregate_with_key(data, aggregation_dict, current_key)

        return aggregation_dict

    def _aggregate_list_with_key(self, data: dict, aggregation_dict: dict, keys: List[str]):
        """
        Utility function that adds the data for all the keys in the list
        to the aggregation dictionary.
        """
        
        for key in keys:
            self._aggregate_with_key(data, aggregation_dict, key)

    def _aggregate_with_key(self, data: dict, aggregation_dict: dict, key: str):
        """
        Utility function that adds the data to the aggregation dictionary.
        """
        
        if not key in aggregation_dict.keys():
            aggregation_dict.setdefault(key, [])

        aggregation_dict[key].append(data)
