from collections.abc import Callable


class DetailsAggregator:
    def __init__(self, data: list, aggregation_key: str):
        self.data = data
        self.aggregation_key = aggregation_key

    def add_column_from_data_column(self, column_name: str, new_column_name: str, fn: Callable):
        for item in self.data:
            if column_name in item.keys():
                column_data = item[column_name]
                item[new_column_name] = fn(column_data)

    def aggregate(self):
        aggregated = {}

        for data in self.data:
            if self.aggregation_key in data.keys():
                current_key = data.get(self.aggregation_key)

                if type(current_key) is list:
                    for key in current_key:
                        self._aggregate_with_key(data, aggregated, key)
                else:
                    self._aggregate_with_key(data, aggregated, current_key)

        return aggregated

    def _aggregate_with_key(self, data: any, aggregated: dict, key: str):
        if not key in aggregated.keys():
            aggregated.setdefault(key, [])

        aggregated[key].append(data)
