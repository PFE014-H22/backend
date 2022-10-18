import csv

input_path = "../BD/QueryResults - questions.csv"
output_path = "../BD/questions.csv"

reader = csv.reader(open(input_path, 'r'))
writer = csv.writer(open(output_path, 'w'))
headers = next(reader)

headers.append("vecteur tf-idf")
print(headers)
writer.writerow(headers)

for row in reader:
    # id = row[0]
    # ici on aurait un call vers le module tf-idf avec le id en param
    # vector = tfidf.getVector(id)
    # apres on append dans chaque row pour l'ecrire dans la derniere colonne
    # row.append(vector)
    
    # row.append(id) # un test pour s'assurer que ca retourne la bonne info

    writer.writerow(row)
