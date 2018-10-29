import original_algorithm.src.globals as GLOB
import random

# TODO fix that the attributes in output are the same as in input
class NodeCluster:
    # TODO cleanup - remove everything network related (I am not using this in my solution)
    # Allow initialization of a new cluster only with a node given
    def __init__(self, node, dataset=None, gen_hierarchies=None, attributes=None, categorical=None, numerical=None):
        self._nodes = [node]
        self._dataset = dataset
        self._genHierarchies = gen_hierarchies
        self._attributes = attributes
        self._categorical = categorical
        self._numerical = numerical
        self._genCatFeatures = {}
        self._genRangeFeatures = {}

        for att in self._attributes:
            if att in self._categorical:
                self._genCatFeatures[att] = self._dataset[node][att]
            elif att in self._numerical:
                self._genRangeFeatures[att] = [self._dataset[node][att], self._dataset[node][att]]

    def get_nodes(self):
        return self._nodes

    def add_node(self, node):
        self._nodes.append(node)

        # Updating feature levels and ranges
        for genCatFeatureKey in self._genCatFeatures:
            self._genCatFeatures[genCatFeatureKey] = self.compute_new_generalization(genCatFeatureKey, node)[1]

        for genRangeFeatureKey in self._genRangeFeatures:
            range = self._genRangeFeatures[genRangeFeatureKey]
            self._genRangeFeatures[genRangeFeatureKey] = self.expand_range(range,
                                                                           self._dataset[node][genRangeFeatureKey])

    def compute_gil(self, node):
        costs = 0.0
        weight_vector = GLOB.GEN_WEIGHT_VECTORS[GLOB.VECTOR]
        # print weight_vector

        for genCatFeatureKey in self._genCatFeatures:
            weight = weight_vector['categorical'][genCatFeatureKey]
            costs += weight * self.compute_categorical_cost(genCatFeatureKey, node)

        for genRangeFeatureKey in self._genRangeFeatures:
            weight = weight_vector['range'][genRangeFeatureKey]
            costs += weight * self.compute_range_cost(genRangeFeatureKey, node)

        return costs  # / float(len(self._genCatFeatures) + len(self._genRangeFeatures))

    def compute_categorical_cost(self, gen_h, node):
        # get the attribute's generalization tree
        cat_hierarchy = self._genHierarchies['categorical'][gen_h]
        cluster_level = self.compute_new_generalization(gen_h, node)[0]
        return float((cat_hierarchy.nr_levels() - cluster_level) / cat_hierarchy.nr_levels())

    def compute_range_cost(self, gen_h, node):
        # size of the interval / size of the original interval
        range_hierarchy = self._genHierarchies['range'][gen_h]
        range_features = self._genRangeFeatures[gen_h]
        node_value = self._dataset[node][gen_h]
        range_cost = range_hierarchy.get_cost_of_range(min(range_features[0], range_features[1], node_value),
                                                       max(range_features[0], range_features[1], node_value))
        return range_cost

    def compute_new_generalization(self, gen_h, node):
        # and node and return level as well as the exact (string) value
        c_hierarchy = self._genHierarchies['categorical'][gen_h]
        n_value = self._dataset[node][gen_h]
        n_level = c_hierarchy.get_level_entry(n_value)
        c_value = self._genCatFeatures[gen_h]
        c_level = c_hierarchy.get_level_entry(c_value)

        while n_value != c_value:
            old_n_level = n_level
            if c_level <= n_level:
                n_value = c_hierarchy.get_generalization_of(n_value)
                n_level -= 1

            # if node and cluster are at the same level, go cluster up too
            if old_n_level <= c_level:
                c_value = c_hierarchy.get_generalization_of(c_value)
                c_level -= 1

        return [c_level, c_value]

    def expand_range(self, range, nr):
        min = nr if nr < range[0] else range[0]
        max = nr if nr > range[1] else range[1]
        return [min, max]

    def compute_node_cost(self, node):
        gil = self.compute_gil(node)  # node is int index of row
        # print "SIL: " + str(sil)
        return GLOB.ALPHA * gil

    def to_string(self):
        out_string = ""

        for count in range(0, len(self._nodes)):
            for att in self._attributes:
                if att in self._numerical:
                    val = self._genRangeFeatures[att]
                    if val[0] == val[1]:
                        out_string += str(val[0]) + ", "
                    else:
                        out_string += "[" + str(val[0]) + " - " + str(val[1]) + "], "

                elif att in self._categorical:
                    out_string += self._genCatFeatures[att] + ", "

                else:
                    node = self._nodes[count]
                    out_string += self._dataset[node][att] + "\n"

        out_string = out_string.replace("all", "*")

        return out_string
