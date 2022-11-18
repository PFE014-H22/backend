import unittest

from src.details.aggregator import DetailsAggregator


class AggregatorTest(unittest.TestCase):
    aggregation_key = "attribute"
    data = [
        {"attribute": "obj_1", "score": 0.5},
        {"attribute": "obj_1", "score": 0.8},
        {"attribute": "obj_2", "score": 0.4, "is_true": True},
        # Next object should not be aggregated because the aggregation key is not in the object (misspelled)
        {"attribut": "obj_3", "score": 0.75}
    ]

    def test_aggregate_by_key(self):
        expected_data = {
            'obj_1': [
                {'attribute': 'obj_1', 'score': 0.5},
                {'attribute': 'obj_1', 'score': 0.8}
            ],
            'obj_2': [
                {'attribute': 'obj_2', 'score': 0.4, 'is_true': True}
            ]
        }

        aggregator = DetailsAggregator(self.data, self.aggregation_key)
        aggregated_data = aggregator.aggretate()
        self.assertEqual(expected_data, aggregated_data)


if __name__ == '__main__':
    unittest.main()
