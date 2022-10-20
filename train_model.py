import csv
import os
from nlp.nlp import NaturalLanguageProcessor
import pickle


def train_model(
    csv_path: str,
    output_path: str
):

    reader = csv.reader(open(csv_path, 'r', encoding='utf8'))
    next(reader)
    text_columns = [0, 3, 4]
    dataset = []
    id_dict = {}
    index = 0
    nlp = NaturalLanguageProcessor()

    print("Reading CSV...")
    for row in reader:
        # ici on recois une liste avec le titre en position 0 et le body en position 1
        text = list(row[i] for i in text_columns)

        id_dict[index] = text[0]
        # ici on aurait un call vers le module tf-idf avec le text en param
        # on combine le titres et le body pour l'instant
        data = f'{text[1]} {text[2]}'
        dataset.append(data)
        index += 1
        # vector = [1, 2, 3, 4, 5]

    print("Training model...")
    nlp.train(dataset, id_dict)

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
