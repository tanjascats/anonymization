import sys

out_dir = '../output/'


def output_csv(clusters, outfile):
    out_string = "age, education-num, capital-gain, capital-loss, workclass, native-country, sex, " \
                 "race, relationship, occupation, marital-status, income\n"
    for cluster in clusters:
        out_string += cluster.to_string()

    csv_output = open(out_dir + outfile, 'w')
    csv_output.write(out_string)
