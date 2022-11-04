import csv
from os import environ
import requests
import time
import pandas as pd

input_path = "../BD/QueryResults.csv"
output_path="./BD/UpdatedResults.csv"

df_csv = pd.read_csv(input_path)

reader = csv.reader(open(input_path, 'r'))
headers = next(reader)
print(headers)
latest = next(reader)

p = '%Y-%m-%d %H:%M:%S'
environ["TZ"] = 'DST'
epoch = int(time.mktime(time.strptime(latest[2], p)))
print(epoch)

current_time = int(time.time())
print(current_time)


def get_questions(page_number: int):
    params = {}
    params["page"] = page_number
    params["filter"] = "!LaSRLv)IebuJjL3K5V4E*n"
    params["min"] = epoch + 1
    params["max"] = current_time
    params["order"] = "desc"
    params["sort"] = "activity"
    params["tagged"] = "cassandra"
    params["site"] = "stackoverflow"
    question_answers_url = f'https://api.stackexchange.com/2.3/questions'
    response = requests.get(question_answers_url, params=params)
    json_response = response.json()
    return json_response


page_number = 1
new_questions = []
while True:
    questions = get_questions(page_number)
    new_questions.extend(questions["items"])
    print(page_number)
    print(questions["has_more"])
    if (questions["has_more"] == False):
        break
    page_number += 1

print(len(new_questions))
print(new_questions[0])
counter = 0
for question in new_questions[:]:
    counter += 1
    try:
        print(question["accepted_answer_id"])
        if (df_csv["Id"].eq(question["question_id"]).any()):
            print("question: " + str(question["question_id"]))
            new_questions.remove(question)
    except:
        new_questions.remove(question)

print(len(new_questions))
print(counter)

print(len(df_csv))

for question in new_questions:
    # to_add = pd.Series([str(question['question_id']), str(question['accepted_answer_id']), str(question['creation_date']), question['title'], question['body'], question['tags']], index=list(df_csv.columns))
    to_add = {
            "Id": str(question['question_id']),
            "AcceptedAnswerId": str(question['accepted_answer_id']),
            "CreationDate": str(question['creation_date']),
            "Title": question['title'],
            "Body": question['body'],
            "Tags": question['tags']
        }

    print(to_add['Id'])
    df_csv = pd.concat([df_csv, pd.DataFrame.from_records([to_add])], ignore_index=True)

print(len(df_csv))

df_csv.to_csv(output_path)
