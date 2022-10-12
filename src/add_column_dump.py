import csv
import pandas as pd

input_path = "../BD/QueryResults - questions.csv"
output_path = "../BD/questions.csv"

reader = csv.reader(open(input_path, 'r'))
writer = csv.writer(open(output_path, 'w'))
headers = next(reader)

headers.append("vecteur tf-idf")
print(headers)
writer.writerow(headers)
for row in reader:
    writer.writerow(row)