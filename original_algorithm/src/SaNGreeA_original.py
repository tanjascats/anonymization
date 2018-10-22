import original_algorithm.src.io.csvInput as csv
import original_algorithm.src.io.output as out
import original_algorithm.src.catGenHierarchy as CGH
import original_algorithm.src.rangeGenHierarchy as RGH
import original_algorithm.src.nodeCluster as CL
import original_algorithm.src.globals as GLOB
import time

# define input file here
adults_csv = '../../data/adult_sample.csv'
#adj_list_csv = '../data/adult_graph_adj_list.csv'
genh_dir = '../../data/gen_hierarchies/'


def prepareGenHierarchiesObject(dataset):
    # Prepare categorical generalization hierarchies
    genh_workclass = CGH.CatGenHierarchy('workclass', genh_dir + 'WorkClassGH.json')
    genh_country = CGH.CatGenHierarchy('native-country', genh_dir + 'NativeCountryBinGH.json')
    genh_sex = CGH.CatGenHierarchy('sex', genh_dir + 'SexGH.json')
    genh_race = CGH.CatGenHierarchy('race', genh_dir + 'RaceGH.json')
    genh_marital = CGH.CatGenHierarchy('marital-status', genh_dir + 'MaritalStatusGH.json')
    genh_occupation = CGH.CatGenHierarchy('occupation', genh_dir + 'OccupationGH.json')
    genh_relationship = CGH.CatGenHierarchy('relationship', genh_dir + 'RelationshipGH.json')

    # Prepare the age range generalization hierarchy
    min_age = float('inf')
    max_age = float('-inf')
    min_edu = float('inf')
    max_edu = float('-inf')
    min_cgain = float('inf')
    max_cgain = float('-inf')
    min_closs = float('inf')
    max_closs = float('-inf')
    min_hpw = float('inf')
    max_hpw = float('-inf')

    # We have to set the age range before instantiating it's gen hierarchy
    # Tanja: Also for every other range attribute
    for idx in dataset:
        idx_age = dataset[idx].get('age')
        idx_edu = dataset[idx].get('education-num')
        idx_cgain = dataset[idx].get('capital-gain')
        idx_closs = dataset[idx].get('capital-loss')
        idx_hpw = dataset[idx].get('hours-per-week')

        min_age = idx_age if idx_age < min_age else min_age
        max_age = idx_age if idx_age > max_age else max_age

        min_edu = idx_edu if idx_edu < min_edu else min_edu
        max_edu = idx_edu if idx_edu > max_edu else max_edu

        min_cgain = idx_cgain if idx_cgain < min_cgain else min_cgain
        max_cgain = idx_cgain if idx_cgain > max_cgain else max_cgain

        min_closs = idx_closs if idx_closs < min_closs else min_closs
        max_closs = idx_closs if idx_closs > max_closs else max_closs

        min_hpw = idx_hpw if idx_hpw < min_hpw else min_hpw
        max_hpw = idx_hpw if idx_hpw > max_hpw else max_hpw

    print("Found age range of: [" + str(min_age) + ":" + str(max_age) + "]")
    print("Found education range of: [" + str(min_edu) + ":" + str(max_edu) + "]")
    print("Found capital gain range of: [" + str(min_cgain) + ":" + str(max_cgain) + "]")
    print("Found capital loss range of: [" + str(min_closs) + ":" + str(max_closs) + "]")
    print("Found hours per week range of: [" + str(min_hpw) + ":" + str(max_hpw) + "]")

    genh_age = RGH.RangeGenHierarchy('age', min_age, max_age)
    genh_edu = RGH.RangeGenHierarchy('education-num', min_edu, max_edu)
    genh_cgain = RGH.RangeGenHierarchy('capital-gain', min_cgain, max_cgain)
    genh_closs = RGH.RangeGenHierarchy('capital-loss', min_closs, max_closs)
    genh_hpw = RGH.RangeGenHierarchy('hours-per-week', min_hpw, max_hpw)

    # Let's create one central object holding all required gen hierarchies
    # to pass around to node clusters during computation
    gen_hierarchies = {
        'categorical': {
            'workclass': genh_workclass,
            'native-country': genh_country,
            'sex': genh_sex,
            'race': genh_race,
            'marital-status': genh_marital,
            'occupation': genh_occupation,
            'relationship': genh_relationship
        },
        'range': {
            'age': genh_age,
            'education-num': genh_edu,
            'capital-gain': genh_cgain,
            'capital-loss': genh_closs,
            'hours-per-week': genh_hpw
        }
    }

    return gen_hierarchies


def main():
    print("Starting SaNGreeA algorithm...")

    ## Prepare io data structures
    adults = csv.readAdults(adults_csv)
#    adj_list = csv.readAdjList(adj_list_csv)
    gen_hierarchies = prepareGenHierarchiesObject(adults)


    ## Main variables needed for SaNGreeA
    clusters = [] # Final output data structure holding all clusters
    best_candidate = None # the currently best candidate by costs
    added = {} # dict containing all nodes already added to clusters

    ## Runtime
    start = time.time()

    ## MAIN LOOP
    for i, node in enumerate(adults):
        if node in added and added[node] == True:
            continue

        # Initialize new cluster with given node
        cluster = CL.NodeCluster(node, adults, gen_hierarchies)

        # Mark node as added
        added[node] = True

        ## SaNGreeA inner loop - Find nodes that minimize costs and
        ## add them to the cluster until cluster_size reaches k
        while len(cluster.getNodes()) < GLOB.K_FACTOR:
            best_cost = float('inf')  # woah
            # candidates from
            for candidate, v in ((k, v) for (k, v) in adults.items() if k > node):
                if candidate in added and added[candidate] == True:
                    continue

                cost = cluster.computeNodeCost(candidate)  # candidate is index of a data row; int
                if cost < best_cost:
                    best_cost = cost
                    best_candidate = candidate

            cluster.addNode(best_candidate)  # index of best candidate
            added[best_candidate] = True

        ## We have filled our cluster with k entries, push it to clusters
        clusters.append(cluster)
        print("\tCluster no." + str(len(clusters)) + " Processed nodes: " + str(i))

    print("Successfully built " + str(len(clusters)) + " clusters.")
    print("Running time: " + str(int(time.time() - start)) + " seconds.")

    out.outputCSV(clusters, "anonymized_" + GLOB.VECTOR + '_weights_k_' + str(GLOB.K_FACTOR) + '.csv')



if __name__ == '__main__':
    main()
