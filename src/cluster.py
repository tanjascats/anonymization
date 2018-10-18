import src.globals as glob


class Cluster:
    # initial_node and node in general is AN INDEX!!!!!!!!
    def __init__(self, initial_node_idx, data):
        self._data = data
        self._nodes_idx = [initial_node_idx]
        self._nodes = [data.get_data().ix[initial_node_idx]]

        self._numerical_att = data.get_numerical()
        self._categorical_att = data.get_categorical()

        self._num_low_bound = self._nodes[0][self._numerical_att]
        self._num_up_bound = self._nodes[0][self._numerical_att]
        self._num_ranges = self.get_num_ranges()
        # TODO categorical attr

    # NODE IS AN INDEX!!!!
    def add_node(self, node_idx):
        self._nodes_idx.append(node_idx)
        self._nodes.append(self._data[self._numerical_att].ix[node_idx])

    def get_size(self):
        return len(self._nodes)

    def get_num_range(self, attribute):
        # be sure low bound is really low and be sure attribute is numerical
        return self._num_up_bound[attribute] - self._num_low_bound[attribute]

    def get_num_ranges(self):
        ranges = {num_att: self.get_num_range(num_att) for num_att in self._numerical_att}
        return ranges

    """
    calculates the generalization information loss (GIL) 
    """
    # node is an index!!
    # calculating gil
    def calculate_gil(self, node_idx):
        # for each attribute calculate new range the cluster would need
        node = self._data.get_data().ix[node_idx]
        original_ranges = self._data.get_ranges()
        gil = 0
        for num_att in self._numerical_att:
            node_value = node[num_att]
            upper, lower = self._num_up_bound[num_att], self._num_low_bound[num_att]

            if node_value >= lower and node_value <= upper:
                new_range = self._num_ranges[num_att]
            elif node_value < lower:
                new_range = upper - node_value
            elif node_value > upper:
                new_range = node_value - lower

            if original_ranges[num_att] != 0:
                gil += new_range/original_ranges[num_att]
            else:
                gil += 0

        gil /= len(self._numerical_att)
        return gil

    def calculate_ngil(self, node_idx):
        return self.calculate_gil(node_idx)/(self._data.get_size()*self._data.get_num_of_attributes())



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
        # cluster_numerical_attr_range = range necessary for cluster to have when it includes new node
        # for each num_attr:
        #   node_val = ...
        #   cluster_val =
        # GIL_num = sum(cluster_numerical_attr_range/numerical_attribute_range) / number_of_numerical_attributes
        #       + sum(node_categorical_attr_level/categorical_attribute_number_of_levels) / num
        # GIL_cat = ...
        # GIL = GIL_num + GIL_cat

    # giving the node index!!!
    def add_node(self, node_idx):
        # TODO
        self._nodes_idx.append(node_idx)
        node = self._data.get_data().ix[node_idx]
        self._nodes.append(node)
        # update lower bound, upper bound and range
        for num_att in self._numerical_att:
            if self._num_low_bound[num_att] > node[num_att]:
                self._num_low_bound[num_att] = node[num_att]
            if self._num_up_bound[num_att] > node[num_att]:
                self._num_up_bound[num_att] = node[num_att]
        self._num_ranges = self.get_num_ranges()
        # TODO for categorical data

    def to_string(self):
        return self._nodes_idx
