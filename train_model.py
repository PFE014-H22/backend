import csv
import os
from nlp.nlp import NaturalLanguageProcessor
from src.config_parameters.cassandra.fetch_cassandra_parameters import \
    find_parameter
import pickle
import time
import json
import re

CASSANDRA_PARAMETER_FILE = "./src/config_parameters/cassandra/cassandra_parameters.txt"
CSV_COLUMNS = 7

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

    dataset = []
    data_dict = {}
    index = 0
    nlp = NaturalLanguageProcessor()

    start = time.time()

    print("Reading CSV...")
    param_occurrences = {}
    for row in reader:
        raw_data = {}
        raw_data["question_id"] = row[0]
        raw_data["answer_id"] = row[1]
        raw_data["creation_date"] = row[2]
        raw_data["question_title"] = row[3]
        raw_data["question_body"] = row[4]
        raw_data["tags"] = [tag.replace('<', '').replace('>', '') for tag in re.findall('\<.*?\>', row[5])]
        raw_data["response_body"] = row[6]
        raw_data["parameters"] = [param.replace("'", "") for param in re.findall(r"'.*?'", row[7])]
        raw_data["link"] = f"https://stackoverflow.com/a/{raw_data['answer_id']}"
        # ID is used to populate dictionnary
        data_dict[index] = raw_data
        # Title and Body are combined into a single string.
        question_text = f'{row[3]} {row[4]}'
        dataset.append(question_text)
        index += 1

    print(f"Found {len(dataset)} questions with parameters")
    print(f"Found {len(param_occurrences)} unique parameters")
    print(json.dumps(param_occurrences, indent=4))
    # Model is trained.
    print("Training model...")
    nlp.train(dataset, data_dict)

    print("Saving model file...")
    # Existing model file is replaced.
    if os.path.exists(output_path):
        os.remove(output_path)

    with open(output_path, 'wb') as output:
        pickle.dump(nlp, output, pickle.HIGHEST_PROTOCOL)

    end = time.time()
    print(f"Time: {end - start} seconds")


if __name__ == "__main__":
    QUERY_RESULTS_PATH = "BD/QueryResults.csv"
    MODEL_PATH = "BD/model.pickle"

    train_model(
        csv_path=QUERY_RESULTS_PATH,
        output_path=MODEL_PATH
    )
