import csv

input_path = "../BD/QueryResults - questions.csv"
output_path = "../BD/questions.csv"

reader = csv.reader(open(input_path, 'r'))
writer = csv.writer(open(output_path, 'w'))
headers = next(reader)

headers.append("vecteur tf-idf")
print(headers)
writer.writerow(headers)
text_columns = [3, 4]

for row in reader:
    # ici on recois une liste avec le titre en position 0 et le body en position 1
    text = list(row[i] for i in text_columns)

    # ici on aurait un call vers le module tf-idf avec le text en param
    # vector = tfidf.getVector(text)
    vector = 1234

    # apres on append dans chaque row pour l'ecrire dans la derniere colonne
    row.append(vector)
    
    # row.append(text[0]) # un test pour s'assurer que ca retourne la bonne info

    writer.writerow(row)
