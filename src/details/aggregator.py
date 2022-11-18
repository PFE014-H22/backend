class DetailsAggregator:
    def __init__(self, data: list, aggregation_key: str):
        self.data = data
        self.aggregation_key = aggregation_key

    def aggretate(self):
        aggregated = {}

        for data in self.data:
            if self.aggregation_key in data.keys():
                current_key = data.get(self.aggregation_key)

                if not current_key in aggregated.keys():
                    aggregated.setdefault(current_key, [])

                aggregated[current_key].append(data)

        return aggregated
