import pickle
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from requests import Response
from nlp.nlp import NaturalLanguageProcessor
from src.answers import get_answers

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
def search():
    query = request.args.get("q", default="", type=str)
    print(f"GET /search?q={query}")

    cosine_similarities, related_indexes = nlp.search([query])

    similarity_scores = [cosine_similarities[index]
                         for index in related_indexes]

    question_ids = [nlp.id_dict[index] for index in related_indexes]
    answers = []
    for i, question_id in enumerate(question_ids):
        data = get_answers(question_id)
        if data:
            answer = data[0]
            answer = {
                "question_id": question_id,
                "answer_id": answer["answer_id"],
                "is_accepted": answer["is_accepted"],
                "link": answer["link"],
                "similarity_score": similarity_scores[i]
            }
            answers.append(answer)

    response = {
        "answers": answers,
        "query": query
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
