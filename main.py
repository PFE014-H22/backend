import pickle

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from requests import Response
from nlp.nlp import NaturalLanguageProcessor

from src.answers import get_answers
from src.SO.so_utils import generate_questions_csv, get_questions

QUERY_RESULTS_PATH = "./BD/QueryResults.csv"
MODEL_PATH = "./BD/model.pickle"

print("Loading model...")
with open(MODEL_PATH, 'rb') as file:
    nlp: NaturalLanguageProcessor = pickle.load(file)
print("Model loaded")
load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, Flask!"


@app.route("/answers/<question_id>", methods=['GET'])
def answers(question_id: int) -> Response:
    print(f"GET /answers/{question_id}")
    answers = get_answers(question_id)
    return jsonify(answers)


@app.route("/search", methods=['GET'])
def hello_there():
    query = request.args.get("q", default="", type=str)
    print(f"GET /search?q={query}")

    cosine_similarities, related_indexes = nlp.search([query])

    question_ids = [nlp.id_dict[index] for index in related_indexes]
    print(question_ids)
    questions = []
    for id in question_ids:
        questions.append(get_answers(id))

    response = {
        "query": query,
        # "cosine_similarities": cosine_similarities.tolist(),
        "question_ids": question_ids,
        "questions": questions
        # "relatedQuestions": [
        #     random.choice(questions),
        #     random.choice(questions),
        # ]
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
