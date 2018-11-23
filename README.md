# k-anonymity with SaNGreeA
SaNGreeA is a Social Network Greedy Anonymization algorithm based on the concept of greedy clustering. Its input is given in the form of a list of feature vectors.

In order to compute its clusters, SaNGreeA takes into account a distance measure (cost function) from clusters to nodes / between 2 nodes:
the Generalization Information Loss (GIL), which measures the degree to which the features of a cluster would have to be generalized in order to incorporate a new node.

### Input data

* the [adult dataset](https://archive.ics.uci.edu/ml/datasets/Adult) as feature vector input for our GIL computations
	* preprocessed [CSV file](https://github.com/tanjascats/anonymization/data/adult_all.csv) for the purposes of multi-class classification on target 'marital-status'
  * preprocessed [CSV file](https://github.com/tanjascats/anonymization/tree/master/data/adult_grouped.csv) for the purposes of multi-class classification on target 'education-num'
* generalization hierarchies in the form of json files
	* which can be found in the gen hierarchy [folder](https://github.com/tanjascats/anonymization/tree/master/data/gen_hierarchies)
* configuration file found in the [folder](https://github.com/tanjascats/anonymization/tree/master/config) with information of:
  * anonymization k-factor
  * target attribute
  * input dataset
  * output folder
  * weight settings
  
### Output data

The structure of a sample output file can be seen [here](https://github.com/tanjascats/anonymization/blob/master/data/output/samples/anonymized_equal_weights_k_7.csv) - '*' stands for maximum generalization (and therefore loss), all other entries can be looked up in the respective generalization hierarchy json files. Depending on which attribute we chose as a target, that column stays unchanged in the output.

### High-level algorithm walkthrough

The following steps would be taken given only the raw adults.csv input file:

1. Read in the CSV, preprocessing / omitting erroneous entries
2. Instantiating generalization hierarchies for categorical values ('Italy' => 'Western Europe') as well as range values ([38-50] + 35 => [35-50])
3. Iterating over the dataset (1.), we execute the following steps:
    * Initialize a new cluster with the given node
    * While the cluster size is smaller k:
      * choose the node from the dataset with the best (lowest) total cost and add it to the cluster
4. If the last cluster is smaller in size than k, we disperse it's members among the previously computed clusters

### Code structure

* config/ - configuration files as described above
* data/ - input data as well as output data as described above
* notebooks/ - Jupyter notebooks containing classification pipelines and results
* papers/ - contains the original SaNGreeA paper and the paper with sample results of classifier behavior on anonymized data
* src/
  * io/
    * csvInput.py - file to read .csv files into python dicts
    * jsonInput.py - file to read .json files into python dicts
    * output.py - file to write the resulting cluster structure to a .csv file
  * catGenHierarchy.py - class to read .json based generalization hierarchy files and compute individual category generalization costs
  * rangeGenHierarchy.py - class to compute individual range generalization costs
  * config.py - central settings file, giving the following options
    * K_FACTOR - the minimum cluster size
    * TARGET - the column of the dataset to stay unchanged (we use this column for latter classification task)
    * GEN_WEIGHT_VECTORS - 3 different pre-settings for feature weights
    * VECTOR - the one setting chosen for a given run
  * SaNGreeA.py - the main file: prepares input structures, runs the main loop, prints results
  * nodeCluster.py - Representing the anonymized clusters of size **k**, this class is responsible for computing the GIL cost function in order to find the next best candidate node.
  * group_edu_num.py - script that prepares the original dataset for anonymization for purposes of multi-class classification on target 'education-num'
  * performance_comparison.py - script that visualizes all results of classifier behavior
* main.py - runs the algorithm with the defined configuration file 


Tanja Šarčević, November 2018, TU Wien
