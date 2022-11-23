import unittest

from src.details.details import Details
from src.details.similarity_score_strategy import SimilarityScoreStrategy


class DetailsTest(unittest.TestCase):
    def setUp(self):
        self.data = {
            'connection_size': [
                {
                    "answer_id": 8705014,
                    "link": 'link1',
                    "question_body": '<p>I tried to to this but it did not work, what am i doing wrong?</p>',
                    "question_id": '8703370',
                    "question_title": 'How do i do this?',
                    "response_body": '<p>You are a dumbass nobody does it this way</p>\n',
                    "similarity_score": 0.21544325589298968,
                    "source_name": 'stackoverflow',
                    "tags": ['Tag 1', 'Tag 2', 'Tag 3'],
                },
                {
                    "answer_id": 8705015,
                    "link": 'link2',
                    "question_body": '<p>This is the end, hold your breath and count to then</p>',
                    "question_id": '8703371',
                    "question_title": 'Skyfall',
                    "response_body": '<p>Feel the Earth move and then, Hear my heart burst again</p>\n',
                    "similarity_score": 0.75,
                    "source_name": 'stackoverflow',
                    "tags": ['Tag 4', 'Tag 2', 'Tag 3'],
                },
            ],
        }

    def test_details(self):
        expected_details = {
            'parameter': {
                'description': 'lorem ipsum',
                'matches': 2,
                'name': 'connection_size'
            },
            'similarity_score': 0.75,
            'sources': [
                {
                    'answer_id': 8705014,
                    'link': 'link1',
                    'question_body': '<p>I tried to to this but it did not work, what am i doing wrong?</p>',
                    'question_id': '8703370',
                    'question_title': 'How do i do this?',
                    'response_body': '<p>You are a dumbass nobody does it this way</p>\n',
                    'similarity_score': 0.21544325589298968,
                    'source_name': 'stackoverflow',
                    'tags': ['Tag 1', 'Tag 2', 'Tag 3']
                },
                {
                    'answer_id': 8705015,
                    'link': 'link2',
                    'question_body': '<p>This is the end, hold your breath and count to then</p>',
                    'question_id': '8703371',
                    'question_title': 'Skyfall',
                    'response_body': '<p>Feel the Earth move and then, Hear my heart burst again</p>\n',
                    'similarity_score': 0.75,
                    'source_name': 'stackoverflow',
                    'tags': ['Tag 4', 'Tag 2', 'Tag 3']
                }
            ]
        }

        for parameter in self.data:
            details = Details(
                self.data[parameter],
                parameter,
                "lorem ipsum",
                SimilarityScoreStrategy.HIGHEST,
                [
                    'answer_id',  'link',  'question_body', 'question_id', 'question_title',
                    'response_body', 'similarity_score', 'source_name', 'tags'
                ]
            )
            actual_details = details.to_json()
            self.assertEqual(expected_details, actual_details)


if __name__ == '__main__':
    unittest.main()
