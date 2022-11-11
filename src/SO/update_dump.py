import csv
from os import environ
import requests
import time
import sys
import pandas as pd

sys.path.insert(0, '../config_parameters/cassandra/')
import fetch_cassandra_parameters

input_path = "../../BD/QueryResults.csv"
output_path="../../BD/UpdatedResults.csv"

param_file_path = "../config_parameters/cassandra/cassandra_parameters.txt"


df_csv = pd.read_csv(input_path)

latest = df_csv.tail(1)

print(latest['CreationDate'].values[0])
p = '%Y-%m-%d %H:%M:%S'
environ["TZ"] = 'DST'
epoch = int(time.mktime(time.strptime(latest['CreationDate'].values[0], p)))
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

def get_answers(page_number: int, question_ids: str):
    params = {}
    params["page"] = page_number
    params["filter"] = "!3uwOg-jScb2C0YKOD"
    params["order"] = "desc"
    params["sort"] = "activity"
    params["site"] = "stackoverflow"
    question_answers_url = f'https://api.stackexchange.com/2.3/questions'
    question_answers_url += '/' + question_ids + '/answers'
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
question_ids = ""
for question in new_questions[:]:
    try:
        print(question["accepted_answer_id"])
        if (df_csv["Id"].eq(question["question_id"]).any()):
            print("question: " + str(question["question_id"]))
            new_questions.remove(question)
        else:
            print("good: " + str(question["question_id"]))
            if not question_ids:
                question_ids += str(question["question_id"])
            else:
                question_ids += ';' + str(question["question_id"])
    except:
        new_questions.remove(question)

print(len(new_questions))
print(question_ids)

page_number = 1
new_answers = []
while True:
    answers = get_answers(page_number, question_ids)
    new_answers.extend(answers["items"])
    print(page_number)
    print(answers["has_more"])
    if (answers["has_more"] == False):
        break
    page_number += 1

print(len(new_answers))

for answer in new_answers[:]:
    if (answer['is_accepted'] == False):
        new_answers.remove(answer)
    else:
        params = fetch_cassandra_parameters.find_parameter(answer['body'], param_file_path)
        if not params:
            new_answers.remove(answer)
        else: 
            print(params)

print(len(new_answers))


# print(len(df_csv))

# # sorted_questions = sorted(new_questions, key=itemgetter('creation_date'))

# for question in new_questions:
#     # to_add = pd.Series([str(question['question_id']), str(question['accepted_answer_id']), str(question['creation_date']), question['title'], question['body'], question['tags']], index=list(df_csv.columns))
#     to_add = {
#             "Id": str(question['question_id']),
#             "AcceptedAnswerId": str(question['accepted_answer_id']),
#             "CreationDate": str(question['creation_date']),
#             "Title": question['title'],
#             "Body": question['body'],
#             "Tags": question['tags']
#         }

#     print(to_add['Id'])
#     df_csv = pd.concat([df_csv, pd.DataFrame.from_records([to_add])], ignore_index=True)

# print(len(df_csv))

# df_csv.to_csv(output_path)
