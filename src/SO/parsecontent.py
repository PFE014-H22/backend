import json
import csv

reader = csv.reader(open("../../BD/questions.csv", 'r'))
headers = next(reader)

for row in reader:
    question = {
        "id": row[0],
        "acceptedAnswerId": row[1],
        "creationDate": row[2],
        "title": row[3],
        "body": row[4],
        "tags": row[5],
        "vector": row[6],
    }

    print(json.dumps(question, sort_keys=True, indent=4))
    break
