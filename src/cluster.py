import src.globals as glob


class Cluster:
    # initial_node and node in general is AN INDEX!!!!!!!!
    def __init__(self, initial_node_idx, data, hierarchies):
        self._nodes_idx = [initial_node_idx]
        #print("Nodes: " + str(self._nodes_idx))

        self._data = data
        # The difference from the original is that here the dataset is pandas
        # dataframe instead of dict as in original
        self._dataset = self._data.get_data()
        #print("Dataset: " + str(self._dataset))
        self._nodes = [self._dataset.ix[initial_node_idx]]
        self._gen_hierarchies = hierarchies # dict of hierarchy objects
        self._gen_cat_features = {feature: self._dataset.ix[initial_node_idx][feature]
                                  for feature in data.get_categorical()}
        self._gen_num_features = {feature: [self._dataset.ix[initial_node_idx][feature],
                                            self._dataset.ix[initial_node_idx][feature]]
                                  for feature in data.get_numerical()}

    # NODE IS AN INDEX!!!!
    def add_node(self, node):
        self._nodes_idx.append(node)
        #self._nodes.append(self._data[self._numerical_att].ix[node_idx])

        # Updating feature levels and ranges

        for genCatFeatureKey in self._gen_cat_features:
            self._gen_cat_features[genCatFeatureKey] = self.compute_new_generalization(genCatFeatureKey, node)[1]
        # print self._genCatFeatures

        for genRangeFeatureKey in self._gen_cat_features:
            range = self._gen_cat_features[genRangeFeatureKey]
            self._gen_cat_features[genRangeFeatureKey] = self.expand_range(range,
                                                                           self._dataset.ix[node][genRangeFeatureKey])
        # print self._genRangeFeatures

    def get_size(self):
        return len(self._nodes)

    def compute_gil(self, node):
        costs = 0.0
        # TODO instead of weights divide cost at the end with number of attributes

        for genCatFeatureKey in self._gen_cat_features:
            costs += self.compute_categorical_cost(genCatFeatureKey, node)

        for genRangeFeatureKey in self._gen_num_features:
            costs += self.compute_range_cost(genRangeFeatureKey, node)

        # TODO / number of attributes
        return costs

    def compute_categorical_cost(self, gen_h, node):
        # get the attribute's generalization tree
        cat_hierarchy = self._gen_hierarchies['categorical'][gen_h]
        cluster_level = self.compute_new_generalization(gen_h, node)[0]
        return float((cat_hierarchy.nr_levels() - cluster_level) / cat_hierarchy.nr_levels())

    def compute_range_cost(self, gen_h, node):
        # size of the interval / size of the original interval
        range_hierarchy = self._gen_hierarchies['range'][gen_h]
        range_features = self._gen_num_features[gen_h]
        node_value = self._dataset.ix[node][gen_h]
        range_cost = range_hierarchy.get_cost_of_range(min(range_features[0], range_features[1], node_value),
                                                       max(range_features[0], range_features[1], node_value))
        return range_cost

    def compute_new_generalization(self, gen_h, node):
        # and node and return level as well as the exact (string) value
        c_hierarchy = self._gen_hierarchies['categorical'][gen_h]
        n_value = self._dataset.ix[node][gen_h]
        n_level = c_hierarchy.get_level_entry(n_value)
        c_value = self._gen_cat_features[gen_h]
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

    def to_string(self):
        # TODO
        return str(self._nodes_idx)
