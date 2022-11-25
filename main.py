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
from src.SO.answers import get_answers
from src.config_parameters.technologies import get_all_technologies
from src.details.aggregator import DetailsAggregator
from src.details.details import Details
from src.details.similarity_score_strategy import SimilarityScoreStrategy
from src.SO.update_dump import updateDump
from src.config_parameters.cassandra import fetch_cassandra_parameters


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


def updateDumpSchedule():
    updateDump()

scheduler = BackgroundScheduler()
scheduler.add_job(func=updateDumpSchedule, trigger="interval",
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
    technology = request.args.get("t", default="", type=str)
    print(f"GET /search?q={query}&t={technology}")

    # Model is used to determine questions sorted by highest similarity to query and similarity scores
    cosine_similarities, related_indexes = processor.search(query)
    normalized_scores = processor.normalize_scores(cosine_similarities, 0, 0.8, 0, 0.9)

    questions = []

    for i in related_indexes:
        similarity_score = normalized_scores[i]
        question = processor.data_dict[i]
        new_question = {
            "answer_id": question["answer_id"],
            "link": question["link"],
            "parameters": question["parameters"],
            "question_body": question["question_body"],
            "question_id": question["question_id"],
            "question_title": question["question_title"],
            "response_body": question["response_body"],
            "similarity_score": similarity_score,
            "source_name": get_data_source(question["link"]),
            "tags": question["tags"],
        }
        questions.append(new_question)

    aggregator = DetailsAggregator(questions, "parameters")
    aggregated_data = aggregator.aggregate()

    details_list = []

    for parameter in aggregated_data:
        details = Details(
            aggregated_data.get(parameter), 
            parameter, 
            "lorem ipsum", 
            SimilarityScoreStrategy.LOWEST,
            [
                'answer_id',  'link',  'question_body', 'question_id',
                'question_title', 'response_body', 'similarity_score', 'source_name', 'tags'
            ]
        )
        details_json = details.to_json()
        details_list.append(details_json)

    # Answers are sent as a response
    response = {
        "answers": details_list,
        "query": query,
        "technology": technology
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)