import unittest

from src.details.aggregator import DetailsAggregator


def dummy_fn(value: any):
    return f'{value}123'


class AggregatorTest(unittest.TestCase):
    def setUp(self):
        self.data = [
            {'attribute': 'obj_1', 'score': 0.5, 'values': [1, 2, 3]},
            {'attribute': 'obj_1', 'score': 0.8, 'values': [1, 3]},
            {'attribute': 'obj_2', 'score': 0.4, 'is_true': True, 'values': [1]},
            # Next object should not be aggregated because the aggregation key is not in the object (misspelled)
            {'attribut': 'obj_3', 'score': 0.75, 'values': [2, 3]}
        ]

    def test_aggregate_by_key(self):
        aggregation_key = 'attribute'

        expected_data = {
            'obj_1': [
                {'attribute': 'obj_1', 'score': 0.5, 'values': [1, 2, 3], 'new_attribute': 'obj_1123'},
                {'attribute': 'obj_1', 'score': 0.8, 'values': [1, 3], 'new_attribute': 'obj_1123'}
            ],
            'obj_2': [
                {'attribute': 'obj_2', 'score': 0.4, 'is_true': True, 'values': [1], 'new_attribute': 'obj_2123'}
            ]
        }

        aggregator = DetailsAggregator(self.data, aggregation_key)
        aggregator.add_column_from_data_column('attribute', 'new_attribute', dummy_fn)
        aggregated_data = aggregator.aggregate()
        self.assertEqual(expected_data, aggregated_data)

    def test_aggregate_by_key_list(self):
        aggregation_key = 'values'

        expected_data = {
            1: [
                {'attribute': 'obj_1', 'score': 0.5, 'values': [1, 2, 3], 'new_attribute': 'obj_1123'},
                {'attribute': 'obj_1', 'score': 0.8, 'values': [1, 3], 'new_attribute': 'obj_1123'},
                {'attribute': 'obj_2', 'score': 0.4, 'is_true': True, 'values': [1], 'new_attribute': 'obj_2123'}
            ],
            2: [
                {'attribute': 'obj_1', 'score': 0.5, 'values': [1, 2, 3], 'new_attribute': 'obj_1123'},
                {'attribut': 'obj_3', 'score': 0.75, 'values': [2, 3]}
            ],
            3: [
                {'attribute': 'obj_1', 'score': 0.5, 'values': [1, 2, 3], 'new_attribute': 'obj_1123'},
                {'attribute': 'obj_1', 'score': 0.8, 'values': [1, 3], 'new_attribute': 'obj_1123'},
                {'attribut': 'obj_3', 'score': 0.75, 'values': [2, 3]}
            ]
        }

        aggregator = DetailsAggregator(self.data, aggregation_key)
        aggregator.add_column_from_data_column('attribute', 'new_attribute', dummy_fn)
        aggregated_data = aggregator.aggregate()
        self.assertEqual(expected_data, aggregated_data)


if __name__ == '__main__':
    unittest.main()
