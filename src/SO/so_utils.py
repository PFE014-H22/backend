import csv
import os


def generate_questions_csv(
    input_path: str,
    output_path: str,
):
    if os.path.exists(output_path):
        os.remove(output_path)

    reader = csv.reader(open(input_path, 'r'))
    writer = csv.writer(open(output_path, 'w'))
    headers = next(reader)

    writer.writerow(headers)
    text_columns = [3, 4]

    for row in reader:
        # ici on recois une liste avec le titre en position 0 et le body en position 1
        text = list(row[i] for i in text_columns)

        # ici on aurait un call vers le module tf-idf avec le text en param
        # vector = tfidf.getVector(text)
        vector = [1, 2, 3, 4, 5]

        # apres on append dans chaque row pour l'ecrire dans la derniere colonne
        row.append(vector)

        # row.append(text[0]) # un test pour s'assurer que ca retourne la bonne info

        writer.writerow(row)


def get_questions(input_path: str):
    reader = csv.reader(open(input_path, 'r'))
    headers = next(reader)
    questions = []

    for row in reader:
        questions.append(
            dict(zip(map(_pascalToCamelCase, headers), row))
        )

    return questions


def _pascalToCamelCase(s):
    return s[0].lower() + s[1:]
