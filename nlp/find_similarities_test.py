import unittest

from nlp.nlp import NaturalLanguageProcessor


class TestFindCosineSimilarities(unittest.TestCase):

    corpus1 = [
        'This is the first document.',
        'I love playing with documents',
        'Is this the first document?',
        'This document is the second document.',
        'Documentation is my passion',
        'I enjoy watching documentaries',
        'And this is the third one.',
    ]

    corpus2 = [
        " The blue parrot drove by the hitchhiking mongoose.",
        "The old apple revels in its authority.",
        "There were a lot of paintings of monkeys waving bamboo sticks in the gallery.",
        "Courage and stupidity were all he had.",
        "In hopes of finding out the truth, he entered the one-room library.",
        "They've been runnin around the corner to find that they had traveled back in time.",
        "It's much more difficult to play tennis with a bowling ball than it is to bowl with a tennis ball.",
        "The clock within this blog and the clock on my laptop are 1 hour different from each other.",
        "Two more days and all his problems would be solved.",
        "There were white out conditions in the town; subsequently, the roads were impassable.",
        "It must be five o'clock somewhere."
    ]

    def test_findSimilaritiesInCorpus2(self):
        query = ["You should always keep a clock on yourself while time-traveling, otherwise you might end up in the wrong part of town."]

        nlp = NaturalLanguageProcessor(self.corpus2)
        print(nlp.preprocessed_dataset)
        cosine_similarities, related_product_indices = nlp.search(query)
        print("Cosine similarities:")
        print(cosine_similarities)
        print("Corpus elements sorted by cosine similarities:")
        print([self.corpus2[i] for i in related_product_indices])

        self.assertTrue(True)
