import sqlite3
from src.config_parameters.cassandra import fetch_cassandra_parameters


#get all questions with tag cassandra since last update
def get_questions(page_number: int, last_update: int, current_time: int):
    """Calls StackExchange API to get all questions with new activity since last update

    Args:
        page_number (int): page of the API response, which will be itirated through with that page number

    Returns:
        json_response (json): response of the API
    """
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

# get all answers to string of question ids


def get_answers(page_number: int, question_ids: str):
    """Calls StackExchange API to get all anwers of given question_ids string

    Args:
        page_number (int): page of the API response, which will be itirated through with that page number
        question_ids (str): string containing a series of ids separated by a ;

    Returns:
        json_response: response of the API
    """
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

def updateDump(last_update: int, current_time: int, df_csv, input_path: str, param_file_path: str):
    """Main function of the script, will fetch the last update time from the SQLite DB and update the csv
    """

    #iterate through API until we reach the last page
    page_number = 1
    new_questions = []
    while True:
        questions = get_questions(page_number, last_update, current_time)
        new_questions.extend(questions["items"])
        if (questions["has_more"] == False):
            break
        page_number += 1

    #filter the list of questions to only get the ones with an accepted answer and not already on the csv
    #fill the question_ids string to use in answers API call
    question_ids = ""
    for question in new_questions[:]:
        try:
            print(question["accepted_answer_id"])
            if (df_csv["Id"].eq(question["question_id"]).any()):
                new_questions.remove(question)
            else:
                if not question_ids:
                    question_ids += str(question["question_id"])
                else:
                    question_ids += ';' + str(question["question_id"])
        except:
            new_questions.remove(question)

    #iterate through answers API until we reach last page
    if new_questions:
        page_number = 1
        new_answers = []
        while True:
            answers = get_answers(page_number, question_ids)
            new_answers.extend(answers["items"])
            if (answers["has_more"] == False):
                break
            page_number += 1

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
                    answer['params'] = params

    list_to_add = []
    # merge questions and answers
    for question in new_questions:
        for answer in new_answers:
            if answer['answer_id'] == question['accepted_answer_id']:
                question['answer_body'] = answer['body']
                question['params'] = answer['params']
                list_to_add.append(question)

    current_csv_length = len(df_csv)
    #add questions to the Dataframe before overwriting csv
    for question in list_to_add:
        to_add = {
            'Id': str(question['question_id']),
            'AcceptedAnswerId': str(question['accepted_answer_id']),
            'CreationDate': str(question['creation_date']),
            'Title': question['title'],
            'Body': question['body'],
            'AnswerBody': question['answer_body'],
            'Tags': question['tags'],
            'Params': question['params']
        }
        df_csv = pd.concat(
            [df_csv, pd.DataFrame.from_records([to_add])], ignore_index=True)

    new_csv_length = len(df_csv)
    df_csv.to_csv(input_path, index=False)

    if current_csv_length == new_csv_length :
        return False
    else :
        return True

if __name__ == '__main__':
    updateDump()
