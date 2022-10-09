from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, Flask!"



@app.route("/search", methods=['GET'])
def hello_there():
    query = request.args.get("q", default="", type=str)

    response = {
        "query": query,
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
