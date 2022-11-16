import csv
from os import environ
import requests
import time
import sys
import pandas as pd
import sqlite3

sys.path.insert(0, '../config_parameters/cassandra/')
import fetch_cassandra_parameters

input_path = "../../BD/QueryResults.csv"
output_path = "../../BD/QueryResults.csv"

param_file_path = "../config_parameters/cassandra/cassandra_parameters.txt"

con = sqlite3.connect("../../BD/DOPAMine.db")
cur = con.cursor()

# get timestamp of last update
res = cur.execute("SELECT * FROM UpdateStamp ORDER BY UpdateTime DESC LIMIT 1")
last_update = res.fetchone()[0]
print(last_update)

df_csv = pd.read_csv(input_path)

current_time = int(time.time())
print(current_time)

#get all questions with tag cassandra since last update
def get_questions(page_number: int):
    params = {}
    params["page"] = page_number
    params["filter"] = "!LaSRLv)IebuJjL3K5V4E*n"
    params["min"] = last_update + 1
    params["max"] = current_time
    params["order"] = "desc"
    params["sort"] = "activity"
    params["tagged"] = "cassandra"
    params["site"] = "stackoverflow"
    question_answers_url = f'https://api.stackexchange.com/2.3/questions'
    response = requests.get(question_answers_url, params=params)
    json_response = response.json()
    return json_response

#get all answers to string of question ids
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

#itirate through API until we reach the last page
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

#filter the list of questions to only get the ones with an accepted answer and not already on the csv
#fill the question_ids string to use in answers API call
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

#itirate through answers API until we reach last page
if new_questions:
    page_number = 1
    new_answers = []
    while True:
        answers = get_answers(page_number, question_ids)
        print(answers)
        new_answers.extend(answers["items"])
        print(page_number)
        print(answers["has_more"])
        if (answers["has_more"] == False):
            break
        page_number += 1

    print(len(new_answers))

    #filter API response to keep only the accepted answers
    for answer in new_answers[:]:
        if (answer['is_accepted'] == False):
            new_answers.remove(answer)
        else:
            params = fetch_cassandra_parameters.find_parameter(
                answer['body'], param_file_path)
            if not params:
                new_answers.remove(answer)
            else:
                # can remove
                print(params)

    print(len(new_answers))

list_to_add = []
# merge questions and answers
for question in new_questions:
    for answer in new_answers:
        if answer['answer_id'] == question['accepted_answer_id']:
            question['answer_body'] = answer['body']
            list_to_add.append(question)

print(len(list_to_add))

print(len(df_csv))

#add questions to the Dataframe before overwriting csv
for question in list_to_add:
    to_add = {
        'Id': str(question['question_id']),
        'AcceptedAnswerId': str(question['accepted_answer_id']),
        'CreationDate': str(question['creation_date']),
        'Title': question['title'],
        'Body': question['body'],
        'AnswerBody': question['answer_body'],
        'Tags': question['tags']
    }

    print(to_add['Id'])
    df_csv = pd.concat(
        [df_csv, pd.DataFrame.from_records([to_add])], ignore_index=True)

print(len(df_csv))

df_csv.to_csv(output_path, index=False)

# insert new updated timestamp
exec_str = "INSERT INTO UpdateStamp VALUES(" + str(current_time) + ");"
res = cur.execute(exec_str)
con.commit()
con.close()
