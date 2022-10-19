from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
import contractions

class NaturalLanguageProcessor:
    # TODO: Read/Write dataset/model to file

    def __init__(self, dataset):
        self.preprocessed_dataset = self.preprocess(dataset)
        self.model = TfidfVectorizer().fit(self.preprocessed_dataset)
        self.model_vector = self.model.transform(self.preprocessed_dataset)
    
    # Find the most similar sentence in the corpus to the query
    def search(self, query: list[str]):
        query = self.preprocess(query)
        query_vector = self.model.transform(query)
        cosine_similarities = cosine_similarity(query_vector, self.model_vector).flatten()
        related_product_indices = cosine_similarities.argsort()[:-11:-1]
        return cosine_similarities, related_product_indices

    # Preprocess a dataset
    def preprocess(self, input: list[str]):
        return [self.lemmatize(self.array_to_string(self.remove_stop_words(self.expand_contractions(sentence.lower())))) for sentence in input]

    # Expand contractions
    def expand_contractions(self, input: str):
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
    def lemmatize(self, input: str):
        nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
        doc = nlp(input)
        return (" ".join([token.lemma_ for token in doc if token.pos_ != 'PUNCT']))

    # Remove stop words from a sentence
    def remove_stop_words(self, input: str):
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(input)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        return filtered_sentence

    # Vectorize a dataset
    def vectorize(self ,input: str):
        vectorizer = TfidfVectorizer()
        vector = vectorizer.fit_transform(input)
        feature_names = vectorizer.get_feature_names_out()
        return vector, feature_names

    # Convert an array of strings to a single string
    def array_to_string(self, array: str):
        return ' '.join(array)
