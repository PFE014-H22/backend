import csv

from src.config_parameters.technologies import find_parameter

def filterDump():
    """Main function of the filter script, this script is only call once at the beginning of the project
    We download the csv from the DataExplorer and filter through it to only keep the answers with cassandra parameters
    """
    input_path = "../../BD/QueryResults.csv"
    output_path = "../../BD/QueryResults_1.csv"

    param_file_path = "../config_parameters/cassandra/cassandra_parameters.txt"

    reader = csv.reader(open(input_path, 'r'))
    writer = csv.writer(open(output_path, 'w'))

    headers = next(reader)
    headers.append("Params")

    print(headers)
    writer.writerow(headers)
    answer_index = 6
    counter = 0

    for row in reader:
        # ici on prends le body de la reponse
        text = row[6]
        # print(text)

        # on recoit une liste contenant tout les params cassandra
        params = find_parameter(row[answer_index], param_file_path)
        if params:
            counter += 1
            row.append(params)
            writer.writerow(row)
            # print(params)

    print("counter: " + str(counter))

if __name__ == '__main__':
    filterDump()
