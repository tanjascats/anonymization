import src.dataset as ds
import src.globals as glob

"""
Input: k, dataset
Output: clustered dataset satisfying k-anonymity with optimized cost measure
"""
# TODO go from simple to better arrangement
data = ds.Dataset()
k = glob.K


"""
calculates the generalization information loss (GIL) 
"""
def calculate_cost(node, cluster):
    # I need:
    # number of range attributes (numerical) -> len(data.numerical)
    # number of categorical attributes -> len(data.categorical)
    # general range of each numerical attribute -> data.ranges.numerical
    # number of hierarchy levels for each categorical value -> data.ranges.categorical
    # the attribute values of each node numerical -> data.at(node).numerical
    # range of the cluster for each numerical attribute -> cluster.ranges
    # generalization levels of the node's categorical attributes ->  data.at(node).categorical
    # generalization levels of the cluster's categorical attributes -> cluster.levels
    # TODO test
    return 1

    pass


def run():
    clusters = []  # final output of the algorithm
    undistributed = data._dataset.index.tolist()  # nodes added to some of the clusters; could be dict TODO
    remains = []

    while len(undistributed) >= 3:  # node is an index
        node = undistributed[0]
        # each cluster will at this point be full because of inner loop
        cluster = [node]  # initializing cluster with a node
        undistributed.remove(node)  # mark node as added
        # now start adding remaining nodes to the cluster until the cluster is big enough
        while len(cluster) < k:
            # we need to find whe node with best cost
            best_cost = float('inf')  # set best cost to infinity
            # iterate over undistributed
            for candidate in undistributed:
                # calculate their shittiness
                curr_cost = calculate_cost(candidate, cluster)
                if curr_cost < best_cost:
                    best_cost = curr_cost
                    best_candidate = candidate

            cluster.append(best_candidate)
            undistributed.remove(best_candidate)

        # add cluster
        clusters.append(cluster)

    # if the last cluster stay of size less than k
    for node in undistributed:
        # find the best cluster to fit node into
        best_cost = float('inf')
        for cluster in clusters:
            curr_cost = calculate_cost(node, cluster)
            if curr_cost < best_cost:
                best_cost = curr_cost
                best_candidate = cluster

        clusters.remove(best_candidate)
        best_candidate.append(node)
        clusters.append(best_candidate)

    return clusters


def main():
    clusters = run()
    print(clusters)


if __name__ == '__main__':
    main()
