import pickle

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from requests import Response

from datasource.datasource import get_data_source
from nlp.nlp import NaturalLanguageProcessor
from src.config_parameters.cassandra.fetch_cassandra_parameters import \
    find_parameter
from src.SO.answers import get_answers

# Path to the pre-trained model
MODEL_PATH = "./BD/model.pickle"
CASSANDRA_PARAMETER_FILE = "./src/config_parameters/cassandra/cassandra_parameters.txt"

# Model is loaded into NLP object
print("Loading model...")
with open(MODEL_PATH, 'rb') as file:
    processor: NaturalLanguageProcessor = pickle.load(file)
print("Model loaded")

load_dotenv()
app = Flask(__name__)


@app.route("/")
def home():
    """Basic home route

    Returns:
        str: "Hello, Flask!"
    """
    return "Hello, Flask!"


@app.route("/answers/<question_id>", methods=['GET'])
def answers(question_id: int) -> Response:
    """Fetches answers from question ids.


    Args:
        question_id (int): Id of the question from which answers are fetched.

    Returns:
        Response: Fetched answers.
    """
    print(f"GET /answers/{question_id}")
    answers = get_answers(question_id)
    return jsonify(answers)


@app.route("/search", methods=['GET'])
def search():
    """Searches for configuration parameters based on user query.

    Returns:
        Response: (TODO) Configuration parameters.
    """
    query = request.args.get("q", default="", type=str)
    print(f"GET /search?q={query}")

    # Model is used to determine questions sorted by highest similarity to query and similarity scores
    cosine_similarities, related_indexes = processor.search(query)
    normalized_scores = processor.normalize_scores(cosine_similarities, 0, 0.8, 0, 0.9)

    # Corresponding answers to each similar questions are fetched
    answers = []
    for i in related_indexes:
        similarity_score = normalized_scores[i]
        question = processor.data_dict[i]
        answer = {
            "question_id": question["question_id"],
            "answer_id": question["answer_id"],
            "similarity_score": similarity_score,
            "parameters": question["parameters"],
            "question_title": question["question_title"],
            "question_body": question["question_body"],
            "response_body": question["response_body"],
            "tags": question["tags"], #add tags from pickle
            "parameters": question["parameters"],
            "link": question["link"]
        }
        answers.append(answer)

    # Answers are sent as a response
    response = {
        "answers": answers,
        "query": query
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
