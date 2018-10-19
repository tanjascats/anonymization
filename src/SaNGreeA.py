import src.globals as glob
import src.cluster as cl
import src.dataset as ds
import src.utils as utils
import src.hierarchy as hie
import time

"""
Input: k, dataset
Output: clustered dataset satisfying k-anonymity with optimized cost measure
"""
# TODO go from simple to better arrangement


def run(data, k, hierarchies):
    start = time.time()
    print("Starting SaNGreeA algorithm with k=" + str(k) + ", " + str(data.get_size()) + " nodes and " +
          str(data.get_num_of_attributes()) + " attributes...")
    clusters = []  # final output of the algorithm
    undistributed = data.get_data().index.tolist()  # INDICES
    remains = []

    while len(undistributed) >= k:  # node is an index
        node = undistributed[0]  # INDEX
        # each cluster will at this point be full because of inner loop
        cluster = cl.Cluster(node, data, hierarchies)  # initializing cluster with a node

        undistributed.remove(node)  # mark node as added
        # now start adding remaining nodes to the cluster until the cluster is big enough
        while cluster.get_size() < k:
            # we need to find whe node with best cost
            best_cost = float('inf')  # set best cost to infinity
            # iterate over undistributed
            best_candidate_idx = undistributed[0]
            for candidate in undistributed:  # candidate is INDEX
                # calculate their shittiness
                # TODO
                # curr_cost = cluster.calculate_gil(candidate)
                curr_cost = cluster.calculate_cat_gil(candidate)

                if curr_cost < best_cost:
                    best_cost = curr_cost
                    best_candidate_idx = candidate

            cluster.add_node(best_candidate_idx)
            undistributed.remove(best_candidate_idx)

        # add cluster
        clusters.append(cluster)

    # if the last cluster stay of size less than k
    for node in undistributed:  # node is INDEX
        # find the best cluster to fit node into
        best_cost = float('inf')
        best_candidate = clusters[0]  # OBJECT cluster
        for cluster in clusters:  # cluster is an object CLUSTER
            curr_cost = cluster.calculate_gil(node)
            if curr_cost < best_cost:
                best_cost = curr_cost
                best_candidate = cluster

        # i need to add node to the best candidate cluster
        clusters.remove(best_candidate)
        best_candidate.add_node(node)
        clusters.append(best_candidate)
    print("Done!\n - Found " + str(len(clusters)) + " clusters." +
          "\n - Running time: " + str(int(time.time()-start)) + " seconds.")
    return clusters

def generate_hierarchies(data):
    # attribute and file path for each hie object
    attributes = data.get_categorical()
    file_paths = glob.HIERARCHY_FILE_PATHS
    hierarchies = {}
    for attribute in attributes:
        hierarchies[attribute] = hie.Hierarchy(attribute, file_paths[attribute])
    return hierarchies


def main():
    # initialize dataset
    data = ds.Dataset()
    # initialize hierarchies
    # TODO
    hierarchies = generate_hierarchies(data)
    # define k
    k = glob.K
    # run algorithm
    clusters = run(data, k, hierarchies)
    # output
    print("Clusters:")
    for c in clusters:
        print(c.to_string())


if __name__ == '__main__':
    main()
