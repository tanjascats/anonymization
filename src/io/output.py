import src.config as config

out_dir = config.OUTPUT_DIR


def output_csv(clusters, columns, outfile):
    out_string = ""
    for i, col in enumerate(columns):
        if i:
            out_string += ", "
        out_string += str(col)
    out_string += "\n"
    for cluster in clusters:
        out_string += cluster.to_string()

    csv_output = open(out_dir + outfile, 'w')
    csv_output.write(out_string)


def output_stats(clusters, end_time, adults, outfile):
    out_string = ""
    out_string += "Anonymized Adult dataset with " + str(len(adults.items())) + " entries and 12 attributes.\n"
    out_string += "k=" + str(config.K_FACTOR) + "\n"
    out_string += "Target attribute: " + str(config.TARGET) + "\n"
    out_string += "Attribute weights: " + config.VECTOR + "\n"
    out_string += "Successfully built " + str(len(clusters)) + " clusters.\n"
    out_string += "Running time: " + str(end_time) + " seconds.\n"

    output = open(out_dir + outfile, 'w')
    output.write(out_string)
