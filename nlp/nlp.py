from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
import contractions


class NaturalLanguageProcessor:

    def __init__(self, dataset=None, id_dict=None):
        if dataset is not None:
            self.id_dict = id_dict
            self.preprocessed_dataset = self.preprocess(dataset)
            self.model = TfidfVectorizer().fit(self.preprocessed_dataset)
            self.model_vectors = self.model.transform(
                self.preprocessed_dataset)

    def train(self, dataset, id_dict):
        self.id_dict = id_dict
        self.preprocessed_dataset = self.preprocess(dataset)
        self.model = TfidfVectorizer().fit(self.preprocessed_dataset)
        self.model_vectors = self.model.transform(self.preprocessed_dataset)

    # Find the most similar sentence in the corpus to the query. Takes str list as input.
    def search(self, query):
        query = self.preprocess(query)
        query_vector = self.model.transform(query)
        cosine_similarities = cosine_similarity(
            query_vector, self.model_vectors).flatten()
        related_product_indices = cosine_similarities.argsort()[:-11:-1]
        return cosine_similarities, related_product_indices

    # Preprocess a dataset. Takes str list as input.
    def preprocess(self, input):
        output = []
        for sentence in input:
            sentence = sentence.lower()
            sentence = self.expand_contractions(sentence)
            sentence = self.remove_stop_words(sentence)
            sentence = self.array_to_string(sentence)
            sentence = self.lemmatize(sentence)
            output.append(sentence)

        return output

    # Expand contractions
    def expand_contractions(self, input):
        expanded_words = []
        suffix = "'s"
        for word in input.split():
            word = contractions.fix(word)
            if word.endswith(suffix):
                word = word[:-len(suffix)]
            expanded_words.append(word)
        expanded_text = ' '.join(expanded_words)
        return expanded_text

    # Lemmatize a sentence
    def lemmatize(self, input):
        nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
        doc = nlp(input)
        return (" ".join([token.lemma_ for token in doc if token.pos_ != 'PUNCT']))

    # Remove stop words from a sentence
    def remove_stop_words(self, input):
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(input)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        return filtered_sentence

    # Vectorize a dataset
    def vectorize(self, input):
        vectorizer = TfidfVectorizer()
        vector = vectorizer.fit_transform(input)
        return vector

    # Convert an array of strings to a single string
    def array_to_string(self, array):
        return ' '.join(array)
