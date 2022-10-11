from flask import Flask, request, jsonify
from dotenv import load_dotenv
from requests import Response
from src.answers import get_answers

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

    response = {
        "query": query,
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
