import src.utils as utils

def main():
    # keys are values of the attribute
    print(utils.read_hierarchy("../data/gen_hierarchies/MaritalStatusGH.json").keys())
    # values of dict are also dict of keys: name, gen and level
    print(utils.read_hierarchy("../data/gen_hierarchies/MaritalStatusGH.json")['Divorced'].keys())


if __name__ == '__main__':
    main()