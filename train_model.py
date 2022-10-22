import csv
import os
from nlp.nlp import NaturalLanguageProcessor
import pickle


def train_model(
    csv_path: str,
    output_path: str
):
    """Trains a nlp model using the NaturalLanguageProcessor class.

    Args:
        csv_path (str): Path to CSV file containing raw dataset.
        output_path (str): Path where pickled model object will we saved.
    """

    reader = csv.reader(open(csv_path, 'r', encoding='utf8'))
    # Header row is skipped
    next(reader)
    # ID, Title and Body columns are selected
    text_columns = [0, 3, 4]

    dataset = []
    id_dict = {}
    index = 0
    nlp = NaturalLanguageProcessor()

    print("Reading CSV...")
    for row in reader:
        # For each row, a list containing the ID, title and body is created.
        text = list(row[i] for i in text_columns)
        # ID is used to populate dictionnary
        id_dict[index] = text[0]
        # Title and Body are combined into a single string.
        data = f'{text[1]} {text[2]}'
        dataset.append(data)
        index += 1

    # Model is trained.
    print("Training model...")
    nlp.train(dataset, id_dict)

    # Existing model file is replaced.
    if os.path.exists(output_path):
        os.remove(output_path)

    print("Saving model file...")
    with open(output_path, 'wb') as output:
        pickle.dump(nlp, output, pickle.HIGHEST_PROTOCOL)


QUERY_RESULTS_PATH = "./BD/QueryResults.csv"
MODEL_PATH = "./BD/model.pickle"

train_model(
    csv_path=QUERY_RESULTS_PATH,
    output_path=MODEL_PATH
)
