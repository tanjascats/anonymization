# this script should be run once on the original Adult dataset in order to
# group the values for attribute education-num
import pandas as pd


def read_data(filepath):
    dataset = pd.read_csv(filepath, sep=r'\s*,\s*', na_values="*", engine='python')
    return dataset


def group_education(dataset):
    dataset1 = dataset.copy()
    # prevent grouping already grouped column
    count = 0
    for i, e in enumerate(dataset1['education-num']):
        if e in range(1, 5):
            dataset1.at[i, 'education-num'] = 1
            count = count + 1
        elif e in range(5, 10):
            dataset1.at[i, 'education-num'] = 2
        elif e in range(10, 14):
            dataset1.at[i, 'education-num'] = 3
        elif e in range(14, 17):
            dataset1.at[i, 'education-num'] = 4
    if count == dataset.shape[0]:
        return dataset
    else:
        return dataset1


# pass directory name inside 'data' directory (no need for full path)
def main():
    filepath = "../data/adult_all.csv"

    dataset = read_data(filepath)
    # group education attribute
    dataset = group_education(dataset)
    # write new dataset to file
    target_file = "../data/adult_grouped.csv"
    dataset.to_csv(target_file, sep=",", index=False)
    # log
    print("Done!")

if __name__ == '__main__':
    main()