from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import os
import time
import pickle

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from requests import Response

from datasource.datasource import get_data_source
from nlp.nlp import NaturalLanguageProcessor
from src.config_parameters.cassandra.fetch_cassandra_parameters import \
    find_parameter
from src.SO.answers import get_answers
from src.config_parameters.technologies import get_all_technologies

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


def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval",
                  seconds=int(os.environ['MODEL_UPDATE_INTERVAL_SECONDS']))
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


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


@app.route("/technologies", methods=['GET'])
def technologies() -> Response:
    """Fetches all available technologies to search from.

    Returns:
        Response: List of technologies.
    """
    print(f"GET /technologies")
    technologies = get_all_technologies()
    return jsonify(technologies)


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
    similarity_scores = [cosine_similarities[index]
                         for index in related_indexes]

    # Corresponding answers to each similar questions are fetched
    question_ids = [processor.id_dict[index] for index in related_indexes]
    answers = []
    for i, question_id in enumerate(question_ids):
        data = get_answers(question_id)
        if data:
            answer = data[0]
            answer = {
                "question_id": question_id,
                "answer_id": answer.get("answer_id", 0),
                "is_accepted": answer.get("is_accepted", False),
                "link": answer.get("link", "http://example.com"),
                "source": get_data_source(answer.get("link", "")),
                "similarity_score": similarity_scores[i],
                "parameters": find_parameter(answer.get("body", ""), CASSANDRA_PARAMETER_FILE),
                "body": answer.get("body", ""),
                "tags": ["cassandra"]  # add tags from pickle
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
