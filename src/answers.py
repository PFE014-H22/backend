import requests


def get_answers(question_id: int):
    params = {}
    params["filter"] = '!6VvPDzQywl)na'
    params["order"] = "desc"
    params["site"] = "stackoverflow"
    params["sort"] = "activity"
    question_answers_url = f'https://api.stackexchange.com/2.3/questions/{question_id}/answers'
    response = requests.get(question_answers_url, params=params)
    json_response = response.json()
    return json_response["items"]
