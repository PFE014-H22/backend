import csv
from os import environ
import requests
import time

input_path = "../BD/QueryResults.csv"

reader = csv.reader(open(input_path, 'r'))
headers = next(reader)
latest = next(reader)

p='%Y-%m-%d %H:%M:%S'
environ["TZ"] = 'DST'
epoch = int(time.mktime(time.strptime(latest[2],p)))
print(epoch)

current_time = int(time.time())
print(current_time)

def get_questions(page_number : int):
    params = {}
    params["page"] = page_number
    params["filter"] = "!)riR7Z9)aCIG*XEEFnLY"
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
    if (questions["has_more"] == False) :
        break
    page_number += 1

print(len(new_questions))
print(new_questions[0])
for question in new_questions:
    try:
        print(question["accepted_answer_id"])
    except:
        new_questions.remove(question)

print(len(new_questions))
