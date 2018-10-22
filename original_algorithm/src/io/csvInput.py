import csv

adult_file_name = '../../data/input_sanitized.csv'
adj_list_file_name = '../../data/adult_graph_adj_list.csv'


def readAdults(file_name):
    adult_file = open(file_name, 'r')
    adults_csv = csv.reader(adult_file, delimiter=',')

    # ignore the headers
    next(adults_csv, None)

    # create the dict we need
    adults = {}

    for adult_idx in adults_csv:
        adult = adults[int(adult_idx[0])] = {}
        adult['age'] = int(adult_idx[1])
        adult['workclass'] = adult_idx[2]
        adult['education-num'] = int(adult_idx[3])
        adult['marital-status'] = adult_idx[4]
        adult['occupation'] = adult_idx[5]
        adult['relationship'] = adult_idx[6]
        adult['race'] = adult_idx[7]
        adult['sex'] = adult_idx[8]
        adult['capital-gain'] = int(adult_idx[9])
        adult['capital-loss'] = int(adult_idx[10])
        adult['hours-per-week'] = int(adult_idx[11])
        adult['native-country'] = adult_idx[12]
        adult['income'] = adult_idx[13]

    adult_file.close()
    return adults


def readAdjList(file_name):
    adj_list_file = open(file_name, 'r')
    adj_list_csv = csv.reader(adj_list_file, delimiter=',')

    # create the dict we need
    adj_list = {}

    for adj_idx in adj_list_csv:
        node = adj_list[int(adj_idx[0])] = adj_idx[1:len(adj_idx)-1]

    adj_list_file.close()
    return adj_list


if __name__ == "__main__":
    print(readAdults(adult_file_name))
    print(readAdjList(adj_list_file_name))
