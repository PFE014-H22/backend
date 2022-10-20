import csv
import os
from nlp.nlp import NaturalLanguageProcessor
import pickle


def train_model(
    csv_path: str,
    output_path: str
):

    reader = csv.reader(open(csv_path, 'r'))
    next(reader)
    text_columns = [3, 4]
    dataset = []
    nlp = NaturalLanguageProcessor()

    print("Reading CSV...")
    for row in reader:
        # ici on recois une liste avec le titre en position 0 et le body en position 1
        text = list(row[i] for i in text_columns)

        # ici on aurait un call vers le module tf-idf avec le text en param
        # on combine le titres et le body pour l'instant
        data = f'{text[0]} {text[1]}'
        dataset.append(data)
        # vector = [1, 2, 3, 4, 5]

    print("Training model...")
    nlp.train(dataset)

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
