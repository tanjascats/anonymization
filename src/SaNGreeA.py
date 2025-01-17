import src.io.csvInput as csv
import src.io.output as out
import src.catGenHierarchy as CGH
import src.rangeGenHierarchy as RGH
import src.nodeCluster as CL
import src.config as config
import time


def read_config(config_file):
    file = open(config_file, "r")
    lines = file.read().splitlines()
    config.K_FACTOR = int(lines[0])
    config.TARGET = lines[1]
    config.DATASET_CSV = lines[2]
    config.OUTPUT_DIR = lines[3]
    config.VECTOR = lines[4]
    file.close()


def prepare_gen_hierarchies_object(dataset, numerical, categorical):
    gen_hierarchies_mine = {'categorical': {}, 'range': {}}

    # Prepare categorical attributes
    for cat_att in categorical:
        genh = CGH.CatGenHierarchy(cat_att, config.GENH_DIR + config.GENH_FILE[cat_att])
        gen_hierarchies_mine['categorical'][cat_att] = genh

    # Prepare numerical attributes
    for num_att in numerical:
        column = [dataset[idx].get(num_att) for idx in range(len(dataset))]
        min_val = min(column)
        max_val = max(column)
        print("Found " + str(num_att) + " range of: [" + str(min_val) + ":" + str(max_val) + "]")
        genh = RGH.RangeGenHierarchy(num_att, min_val, max_val)
        gen_hierarchies_mine['range'][num_att] = genh

    return gen_hierarchies_mine


def run(config_file):
    print("Starting SaNGreeA algorithm...")
    read_config(config_file)
    # Prepare io data structures
    # note: columns contain target attribute as well
    adults, columns, numerical, categorical = csv.read_dataset(config.DATASET_CSV)
    print("Dataset containing " + str(len(adults.items())) + " columns.")
    print("k=" + str(config.K_FACTOR))
    print("Target: " + str(config.TARGET))
    print("Attribute weights: " + config.VECTOR + "\n")
    gen_hierarchies = prepare_gen_hierarchies_object(adults, numerical, categorical)

    # Main variables needed for SaNGreeA
    clusters = []  # Final output data structure holding all clusters
    best_candidate = None  # the currently best candidate by costs
    added = {}  # dict containing all nodes already added to clusters

    # Runtime
    start = time.time()

    # MAIN LOOP
    for i, node in enumerate(adults):
        if node in added and added[node] is True:
            continue

        # Initialize new cluster with given node
        cluster = CL.NodeCluster(node, adults, gen_hierarchies, columns, categorical, numerical)

        # Mark node as added
        added[node] = True

        # SaNGreeA inner loop - Find nodes that minimize costs and
        # add them to the cluster until cluster_size reaches k
        while len(cluster.get_nodes()) < config.K_FACTOR:
            best_cost = float('inf')
            # candidates from
            for candidate, v in ((k, v) for (k, v) in adults.items() if k > node):
                if candidate in added and added[candidate] is True:
                    continue

                cost = cluster.compute_node_cost(candidate)  # candidate is index of a data row; int
                if cost < best_cost:
                    best_cost = cost
                    best_candidate = candidate

            cluster.add_node(best_candidate)  # index of best candidate
            added[best_candidate] = True

        # We have filled our cluster with k entries, push it to clusters
        clusters.append(cluster)

    end_time = int(time.time() - start)
    print("Successfully built " + str(len(clusters)) + " clusters.")
    print("Running time: " + str(end_time) + " seconds.")

    print("Output file: " + config.OUTPUT_DIR)
    out.output_csv(clusters, columns, "anonymized_" + config.VECTOR + '_weights_k_' + str(config.K_FACTOR) + '.csv')
    out.output_stats(clusters, end_time, adults, "stats_k_" + str(config.K_FACTOR) + ".txt")


def main():
    run()


if __name__ == '__main__':
    main()
