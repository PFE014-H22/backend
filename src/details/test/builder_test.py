import unittest

from src.details.builder import DetailsBuilder
from src.details.similarity_score_strategy import SimilarityScoreStrategy


class BuilderTest(unittest.TestCase):
    data = {
        'connection_size': [
            {
                "answer_id": 8705014,
                "question_body": '<p>I tried to to this but it did not work, what am i doing wrong?</p>',
                "response_body": '<p>You are a dumbass nobody does it this way</p>\n',
                "is_accepted": True,
                "link": 'link1',
                "name": 'stackoverflow',
                "question_id": '8703370',
                "question_title": 'How do i do this?',
                "similarity_score": 0.21544325589298968,
                "tags": ['Tag 1', 'Tag 2', 'Tag 3'],
            },
            {
                "answer_id": 8705015,
                "question_body": '<p>This is the end, hold your breath and count to then</p>',
                "response_body": '<p>Feel the Earth move and then, Hear my heart burst again</p>\n',
                "is_accepted": False,
                "link": 'link2',
                "name": 'stackoverflow',
                "question_id": '8703371',
                "question_title": 'Skyfall',
                "similarity_score": 0.75,
                "tags": ['Tag 4', 'Tag 2', 'Tag 3'],
            },
        ],
    }

    def test_answer_builder(self):
        expected_answers = {
            'parameter': {
                'name': 'connection_size',
                'description': 'lorem ipsum',
                'matches': 2
            },
            'similarity_score': 0.75,
            'sources': [
                {
                    'answer_id': 8705014,
                    'is_accepted': True,
                    'link': 'link1',
                    'name': 'stackoverflow',
                    'question_body': '<p>I tried to to this but it did not work, what am i doing wrong?</p>',
                    'question_id': '8703370',
                    'question_title': 'How do i do this?',
                    'response_body': '<p>You are a dumbass nobody does it this way</p>\n',
                    'similarity_score': 0.21544325589298968,
                    'tags': ['Tag 1', 'Tag 2', 'Tag 3']
                },
                {
                    'answer_id': 8705015,
                    'is_accepted': False,
                    'link': 'link2',
                    'name': 'stackoverflow',
                    'question_body': '<p>This is the end, hold your breath and count to then</p>',
                    'question_id': '8703371',
                    'question_title': 'Skyfall',
                    'response_body': '<p>Feel the Earth move and then, Hear my heart burst again</p>\n',
                    'similarity_score': 0.75,
                    'tags': ['Tag 4', 'Tag 2', 'Tag 3']
                }
            ]
        }

        for parameter in self.data:
            highest_score = SimilarityScoreStrategy.HIGHEST
            builder = DetailsBuilder(self.data[parameter])
            builder = builder.for_parameter(parameter)
            builder = builder.for_parameter_description("lorem ipsum")
            builder = builder.with_similarity_score_strategy(highest_score)
            answers = builder.build()
            self.assertEqual(expected_answers, answers)


if __name__ == '__main__':
    unittest.main()
