import src.utils as utils
import src.hierarchy as hie


def main():
    # keys are values of the attribute
    hierarchy = utils.read_hierarchy("../data/gen_hierarchies/MaritalStatusGH.json")
    print("Command: utils.read_hierarchy(file).keys()")
    print(utils.read_hierarchy("../data/gen_hierarchies/MaritalStatusGH.json").keys())
    # values of dict are also dict of keys: name, gen and level
    print("Command: utils.read_hierarchy(file)['Divorced'].keys()")
    print(utils.read_hierarchy("../data/gen_hierarchies/MaritalStatusGH.json")['Divorced'].keys())

    hierarchy_class = hie.Hierarchy('marital-status', "../data/gen_hierarchies/MaritalStatusGH.json")
    print(hierarchy_class.get_height())
    print(hierarchy_class.get_level('all'))
    hierarchy_class = hie.Hierarchy('occupation', "../data/gen_hierarchies/OccupationGH.json")
    print(hierarchy_class.get_height())


if __name__ == '__main__':
    main()