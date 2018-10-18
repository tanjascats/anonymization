import src.globals as glob
import src.cluster as cl
import time

"""
Input: k, dataset
Output: clustered dataset satisfying k-anonymity with optimized cost measure
"""
# TODO go from simple to better arrangement
data = glob.DATASET
k = glob.K


def run():
    start = time.time()
    print("Starting SaNGreeA algorithm with k=" + str(k) + ", " + str(data.get_size()) + " nodes and " +
          str(data.get_num_of_attributes()) + " attributes...")
    clusters = []  # final output of the algorithm
    undistributed = data.get_data().index.tolist()  # nodes added to some of the clusters; could be dict TODO
    remains = []

    while len(undistributed) >= 3:  # node is an index
        node = undistributed[0]
        # each cluster will at this point be full because of inner loop
        cluster = cl.Cluster(node)  # initializing cluster with a node
        undistributed.remove(node)  # mark node as added
        # now start adding remaining nodes to the cluster until the cluster is big enough
        while cluster.get_size() < k:
            # we need to find whe node with best cost
            best_cost = float('inf')  # set best cost to infinity
            # iterate over undistributed
            for candidate in undistributed:
                # calculate their shittiness
                curr_cost = cluster.calculate_gil(candidate)
                if curr_cost < best_cost:
                    best_cost = curr_cost
                    best_candidate = candidate

            print(best_cost)
            cluster.add_node(best_candidate)
            undistributed.remove(best_candidate)

        # add cluster
        clusters.append(cluster)

    # if the last cluster stay of size less than k
    for node in undistributed:
        # find the best cluster to fit node into
        best_cost = float('inf')
        for cluster in clusters:
            curr_cost = cluster.calculate_gil(node)
            if curr_cost < best_cost:
                best_cost = curr_cost
                best_candidate = cluster

        clusters.remove(best_candidate)
        best_candidate.append(node)
        clusters.append(best_candidate)
    print("Done!\n - Found " + str(len(clusters)) + " clusters."
                                                   "\n - Running time: " + str(int(time.time()-start)) + " seconds.")
    return clusters


def main():
    clusters = run()
    print(clusters)


if __name__ == '__main__':
    main()
