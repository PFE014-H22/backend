from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
import contractions


class NaturalLanguageProcessor:
    """Natural language processing class which offers tool to preprocess text-based datasets as well as train a text similiarity classifier based on a TF-IDF algorithm"""

    def __init__(self, dataset=None, data_dict=None):
        """Class constructor. Initializes object fields and trains model if dataset and dictionnary are given.

        Args:
            dataset (list[str], optional): Training dataset. Defaults to None.
            data_dict (dict[int, int], optional): Dictionary with indexes as keys and raw_data as values. Defaults to None.
        """
        if dataset and data_dict:
            self.data_dict = data_dict
            self.preprocessed_dataset = self.preprocess(dataset)
            self.model = TfidfVectorizer().fit(self.preprocessed_dataset)
            self.model_vectors = self.model.transform(
                self.preprocessed_dataset)

    def train(self, dataset, data_dict, update=False):
        """Trains model with given dataset and dictionnary.

        Args:
            dataset (list[str], optional): Training dataset. Defaults to None.
            data_dict (dict[int, int], optional): Dictionary with indexes as keys and raw_data as values. Defaults to None.
        """
        if update:
            self.data_dict.update(data_dict)
            self.preprocessed_dataset.extend(self.preprocess(dataset))
        else:
            self.data_dict = data_dict
            self.preprocessed_dataset = self.preprocess(dataset)
            
        self.model = TfidfVectorizer().fit(self.preprocessed_dataset)
        self.model_vectors = self.model.transform(self.preprocessed_dataset)

    def search(self, query):
        """Queries the trained model with input and returns indexes of the most similar sentences as well as cosine similarity scores.

        Args:
            query (str): Text string used by the model to determine closest matches.

        Returns:
            ndarray: List of all similarity scores with query.
            ndarray: Indexes of 10 highest similarities.
        """
        query = self.preprocess([query])
        query_vector = self.model.transform(query)
        cosine_similarities = cosine_similarity(
            query_vector, self.model_vectors).flatten()
        related_product_indices = cosine_similarities.argsort()[:-11:-1]
        return cosine_similarities, related_product_indices

    def preprocess(self, input):
        """Preprocesses text by removing unnecessary words and characters. Includes lowercasing, contraction and stop words removal, as well as lemmatization.

        Args:
            input (list[str]): List of string inputs to be preprocessed.

        Returns:
            list[str]: List of preprocessed strings.
        """
        output = []
        for sentence in input:
            sentence = sentence.lower()
            sentence = self.expand_contractions(sentence)
            sentence = self.remove_stop_words(sentence)
            sentence = self.array_to_string(sentence)
            sentence = self.lemmatize(sentence)
            output.append(sentence)

        return output

    def expand_contractions(self, input):
        """Expands english contractions into the full two words they are composed from (e.g.: "They've" becomes "They have").

        Args:
            input (str): Text input.

        Returns:
            str: Processed text.
        """
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
        """Lemmatizes every word in the given english text sentence into their basic form (e.g.: "Gifted" and "Gifts" both become "Gift") while also removing punctuation.

        Args:
            input (str): Text input.

        Returns:
            str: Processed text.
        """

        nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
        doc = nlp(input)
        return (" ".join([token.lemma_ for token in doc if token.pos_ != 'PUNCT']))

    def remove_stop_words(self, input):
        """Removes stop words from the given english text input (e.g.:"the", "a", "is").

        Args:
            input (str): Text input.

        Returns:
            str: Processed text.
        """
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(input)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        return filtered_sentence

    def vectorize(self, input):
        """Converts given text into vector using TF-IDF algorithm.

        Args:
            input (str): Text input.

        Returns:
            ndarray: Vector of TF-IDF scores.
        """
        vectorizer = TfidfVectorizer()
        vector = vectorizer.fit_transform(input)
        return vector

    def array_to_string(self, array):
        """Converts an array of strings to a single string.

        Args:
            array (list[str]): List of strings to combine.

        Returns:
            str: Combined strings.
        """
        return ' '.join(array)

    def normalize_scores(self, scores, old_min, old_max, new_min, new_max):
        """Normalizes given scores from old range to new range.

        Args:
            scores (ndarray): List of scores to normalize.

        Returns:
            ndarray: Normalized scores.
        """
        print(scores)
        scores = [(new_max - new_min) * (score - old_min) / ( old_max - old_min ) + new_min for score in scores]
        print(scores)
        return scores
