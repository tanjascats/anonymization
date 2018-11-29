import csv
import matplotlib.pyplot as plt
import pickle

k_values = [-1, 3, 7, 11, 15, 19, 23, 27, 31, 35, 39]


def read_paper_results(filepath):
    # filepath = "../data/paper_results/LR_edu-num_equal.csv"
    input_file = csv.DictReader(open(filepath), fieldnames=["k", "value"])
    points = []
    for i, row in enumerate(input_file):
        if round(float(row['k'])) != k_values[i]:
            print("Something went wrong with k values.  \nk in file: " + str(
                round(float(row['k']))) + "\nk desired: " + str(k_values[i]))
            break
        points.append(float(row['value']))

    return points


# read experiment results -> output/classification-res (pickled)
def load_classification_results(weights, target_attribute):
    if weights != "":
        weights += "_"
    f1_scores_GB = []
    f1_scores_LR = []
    f1_scores_LSVC = []
    f1_scores_RF = []

    for k in k_values:
        # load results
        if k == -1:
            infile = open('../data/output/' + target_attribute + '/classification-res/adult_multiclass_full', 'rb')
        elif k == 39:
            infile = open('../data/output/' + target_attribute + '/classification-res/adult_multiclass_' + weights + 'k100',
                          'rb')
        else:
            infile = open(
                '../data/output/' + target_attribute + '/classification-res/adult_multiclass_' + weights + 'k' + str(k),
                'rb')
        scores = pickle.load(infile)
        infile.close()

        f1_scores_GB.append(scores['Gradient Boosting'])
        if 'Logistic Regression' in scores.keys():
            f1_scores_LR.append(scores['Logistic Regression'])
        elif 'Logistic Regression number-encoded' in scores.keys():
            f1_scores_LR.append(scores['Logistic Regression number-encoded'])
        else:
            f1_scores_LR.append(scores['Logistic Regression binary'])
        if 'Linear SVC' in scores.keys():
            f1_scores_LSVC.append(scores['Linear SVC'])
        else:
            f1_scores_LSVC.append(scores['Linear SVC binary'])
        f1_scores_RF.append(scores['Random Forest'])

    return f1_scores_LR, f1_scores_LSVC, f1_scores_RF, f1_scores_GB


# ----- EDUCATION NUMBER ------
# - paper results
LR_equal_paper = read_paper_results("../data/paper_results/LR_edu-num_equal.csv")
LR_age_paper = read_paper_results("../data/paper_results/LR_edu-num_age.csv")
LR_race_paper = read_paper_results("../data/paper_results/LR_edu-num_race.csv")

LSVC_equal_paper = read_paper_results("../data/paper_results/LSVC_edu-num_equal.csv")
LSVC_age_paper = read_paper_results("../data/paper_results/LSVC_edu-num_age.csv")
LSVC_race_paper = read_paper_results("../data/paper_results/LSVC_edu-num_race.csv")

RF_equal_paper = read_paper_results("../data/paper_results/RF_edu-num_equal.csv")
RF_age_paper = read_paper_results("../data/paper_results/RF_edu-num_age.csv")
RF_race_paper = read_paper_results("../data/paper_results/RF_edu-num_race.csv")

GB_equal_paper = read_paper_results("../data/paper_results/GB_edu-num_equal.csv")
GB_age_paper = read_paper_results("../data/paper_results/GB_edu-num_age.csv")
GB_race_paper = read_paper_results("../data/paper_results/GB_edu-num_race.csv")

# - my results
LR, LSVC, RF, GB = load_classification_results("", "education-num")
LR_age, LSVC_age, RF_age, GB_age = load_classification_results("emph_age", "education-num")
LR_race, LSVC_race, RF_race, GB_race = load_classification_results("emph_race", "education-num")

# - ARX results
# Logistic Regression by sklearn
infile = open('../data/ARX/multi-class-edu/LR_f1_scores', 'rb')
LR_ARX = pickle.load(infile)
infile.close()
# Linear SVC by sklearn
infile = open('../data/ARX/multi-class-edu/SVC_f1_scores', 'rb')
LSVC_ARX = pickle.load(infile)
infile.close()
# Random Forest by Weka
with open("../data/ARX/multi-class-edu/f1_scores_Random_Forest_Weka.txt") as f:
    lines = f.readlines()
RF_ARX = [float(score.rstrip('\n'))/100. for score in lines]
# Gradient Boosting by RapidMiner
filepath = "../data/ARX/multi-class-edu/f1_scores_Gradient_Boosting_RapidMiner.txt"
with open(filepath) as f:
    lines = f.readlines()
GB_ARX = [float(score.rstrip('\n'))/100. for score in lines]

# - visualize
ticks = k_values
xlabels = list(k_values); xlabels[0] = "None"; xlabels[-1] = 100

fig = plt.figure(figsize=(11,11))
#fig.suptitle('Multi-class classification on target education-num', fontsize=16)

# ----- LOGISTIC REGRESSION -----
# --- equal weight - red ---
ax = fig.add_subplot(4,3,1)
ax.set_title('equal weights')
ax.set_xticklabels(xlabels)

line1, = plt.plot(ticks, LR_equal_paper, marker='o', markersize=4, linewidth=1, color='r',
                  label='Results from [2]')
line2, = plt.plot(ticks, LR, marker='o', markersize=4, linewidth=1, color='black', label='Results in this paper')
line3, = plt.plot(ticks, LR_ARX, marker='o', markersize=4, linewidth=1, color='grey', label='Results from ARX')
plt.ylabel('LOGISTIC REGRESSION\n\nF1 score')
plt.xticks(ticks, size=8)
plt.yticks(size=8)
plt.legend(handles=[line1, line2, line3], loc=1, prop={'size': 7})

# --- age preferred - blue ---
ax = fig.add_subplot(4,3,2)
ax.set_title('age preferred')
ax.set_xticklabels(xlabels)

line1, = plt.plot(ticks, LR_age_paper, marker='v', markersize=4, linewidth=1, color='b', label='Results from [2]')
line2, = plt.plot(ticks, LR_age, marker='v', markersize=4, linewidth=1, color='black', label='Results in this paper')
plt.xticks(ticks, size=8)
plt.yticks(size=8)
plt.legend(handles=[line1, line2], loc=1, prop={'size': 7})

# --- race preferred - green ---
ax = fig.add_subplot(4,3,3)
ax.set_title('race preferred')
ax.set_xticklabels(xlabels)

line1, = plt.plot(ticks, LR_race_paper, marker='d', markersize=4, linewidth=1, color='g', label='Results from [2]')
line2, = plt.plot(ticks, LR_race, marker='d', markersize=4, linewidth=1, color='black', label='Results in this paper')
plt.xticks(ticks, size=8)
plt.yticks(size=8)
plt.legend(handles=[line1, line2], loc=1, prop={'size': 7})

# ----- LINEAR SVC -----
# --- equal weights - red ---
ax = fig.add_subplot(4,3,4)
ax.set_xticklabels(xlabels)

plt.plot(ticks, LSVC_equal_paper, marker='o', markersize=4, linewidth=1, color='r')
plt.plot(ticks, LSVC, marker='o', markersize=4, linewidth=1, color='black')
plt.plot(ticks, LSVC_ARX, marker='o', markersize=4, linewidth=1, color='grey')
plt.ylabel('LINEAR SVC\n\nF1 score')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

# --- age preferred - blue ---
ax = fig.add_subplot(4,3,5)
ax.set_xticklabels(xlabels)

plt.plot(ticks, LSVC_age_paper, marker='v', markersize=4, linewidth=1, color='b')
plt.plot(ticks, LSVC_age, marker='v', markersize=4, linewidth=1, color='black')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

# --- race preferred - green ---
ax = fig.add_subplot(4,3,6)
ax.set_xticklabels(xlabels)

plt.plot(ticks, LSVC_race_paper, marker='d', markersize=4, linewidth=1, color='g')
plt.plot(ticks, LSVC_race, marker='d', markersize=4, linewidth=1, color='black')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

# ----- RANDOM FOREST -----
# --- equal weights - red ---
ax = fig.add_subplot(4,3,7)
ax.set_xticklabels(xlabels)

plt.plot(ticks, RF_equal_paper, marker='o', markersize=4, linewidth=1, color='r')
plt.plot(ticks, RF, marker='o', markersize=4, linewidth=1, color='black')
plt.plot(ticks, RF_ARX, marker='o', markersize=4, linewidth=1, color='grey')
plt.ylabel('RANDOM FOREST\n\nF1 score')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

# --- age preferred - blue ---
ax = fig.add_subplot(4,3,8)
ax.set_xticklabels(xlabels)

plt.plot(ticks, RF_age_paper, marker='v', markersize=4, linewidth=1, color='b')
plt.plot(ticks, RF_age, marker='v', markersize=4, linewidth=1, color='black')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

# --- race preferred - green ---
ax = fig.add_subplot(4,3,9)
ax.set_xticklabels(xlabels)

plt.plot(ticks, RF_race_paper, marker='d', markersize=4, linewidth=1, color='g')
plt.plot(ticks, RF_race, marker='d', markersize=4, linewidth=1, color='black')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

# ----- GRADIENT BOOSTING -----
# --- equal weights - red ---
ax = fig.add_subplot(4,3,10)
ax.set_xticklabels(xlabels)

plt.plot(ticks, GB_equal_paper, marker='o', markersize=4, linewidth=1, color='r')
plt.plot(ticks, GB, marker='o', markersize=4, linewidth=1, color='black')
plt.plot(ticks, GB_ARX, marker='o', markersize=4, linewidth=1, color='grey')
plt.ylabel('GRADIENT BOOSTING\n\nF1 score')
plt.xlabel('anonymization k-factor')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

# --- age preferred - blue ---
ax = fig.add_subplot(4,3,11)
ax.set_xticklabels(xlabels)

plt.plot(ticks, GB_age_paper, marker='v', markersize=4, linewidth=1, color='b')
plt.plot(ticks, GB_age, marker='v', markersize=4, linewidth=1, color='black')
plt.xlabel('anonymization k-factor')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

# --- race preferred - green ---
ax = fig.add_subplot(4,3,12)
ax.set_xticklabels(xlabels)

plt.plot(ticks, GB_race_paper, marker='d', markersize=4, linewidth=1, color='g')
plt.plot(ticks, GB_race, marker='d', markersize=4, linewidth=1, color='black')
plt.xlabel('anonymization k-factor')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

# ------ MARITAL STATUS -----
# - results from paper
LR_equal_paper = read_paper_results("../data/paper_results/LR_mar-stat_equal.csv")
LR_age_paper = read_paper_results("../data/paper_results/LR_mar-stat_age.csv")
LR_race_paper = read_paper_results("../data/paper_results/LR_mar-stat_race.csv")

LSVC_equal_paper = read_paper_results("../data/paper_results/LSVC_mar-stat_equal.csv")
LSVC_age_paper = read_paper_results("../data/paper_results/LSVC_mar-stat_age.csv")
LSVC_race_paper = read_paper_results("../data/paper_results/LSVC_mar-stat_race.csv")

RF_equal_paper = read_paper_results("../data/paper_results/RF_mar-stat_equal.csv")
RF_age_paper = read_paper_results("../data/paper_results/RF_mar-stat_age.csv")
RF_race_paper = read_paper_results("../data/paper_results/RF_mar-stat_race.csv")

GB_equal_paper = read_paper_results("../data/paper_results/GB_mar-stat_equal.csv")
GB_age_paper = read_paper_results("../data/paper_results/GB_mar-stat_age.csv")
GB_race_paper = read_paper_results("../data/paper_results/GB_mar-stat_race.csv")

# - my results
LR, LSVC, RF, GB = load_classification_results("", "marital-status")
LR_age, LSVC_age, RF_age, GB_age = load_classification_results("emph_age", "marital-status")
LR_race, LSVC_race, RF_race, GB_race = load_classification_results("emph_race", "marital-status")

# - ARX results
# Linear SVC
filepath = "../data/ARX/multi-class-mar/LSVC"
with open(filepath) as f:
    lines = f.readlines()
LSVC_ARX = [float(score.rstrip('\n')) for score in lines]
# Gradient Boosting by RapidMiner
filepath = "../data/ARX/multi-class-mar/GB"
with open(filepath) as f:
    lines = f.readlines()
GB_ARX = [float(score.rstrip('\n')) for score in lines]
# Logistic Regression
filepath = "../data/ARX/multi-class-mar/LR"
with open(filepath) as f:
    lines = f.readlines()
LR_ARX = [float(score.rstrip('\n')) for score in lines]
# Random Forest
filepath = "../data/ARX/multi-class-mar/RF"
with open(filepath) as f:
    lines = f.readlines()
RF_ARX = [float(score.rstrip('\n')) for score in lines]

# - Visualize
ticks = k_values
xlabels = list(k_values); xlabels[0] = "None"; xlabels[-1] = 100

fig = plt.figure(figsize=(11,11))
#fig.suptitle('Multi-class classification on target marital-status', fontsize=16)

# ----- LOGISTIC REGRESSION -----
# --- equal weight - red ---
ax = fig.add_subplot(4,3,1)
ax.set_title('equal weights')
ax.set_xticklabels(xlabels)

line1, = plt.plot(ticks, LR_equal_paper, marker='o', markersize=4, linewidth=1, color='r', label='Results from [2]')
line2, = plt.plot(ticks, LR, marker='o', markersize=4, linewidth=1, color='black', label='Results in this paper')
line3, = plt.plot(ticks, LR_ARX, marker='o', markersize=4, linewidth=1, color='grey', label='Results from ARX')
plt.ylabel('LOGISTIC REGRESSION\n\nf1 score')
plt.xticks(ticks, size=8)
plt.yticks(size=8)
plt.legend(handles=[line1, line2, line3], loc=1, prop={'size': 7})

# --- age preferred - blue ---
ax = fig.add_subplot(4,3,2)
ax.set_title('age preferred')
ax.set_xticklabels(xlabels)

line1, = plt.plot(ticks, LR_age_paper, marker='v', markersize=4, linewidth=1, color='b', label='Results from [2]')
line2, = plt.plot(ticks, LR_age, marker='v', markersize=4, linewidth=1, color='black', label='Results in this paper')
plt.xticks(ticks, size=8)
plt.yticks(size=8)
plt.legend(handles=[line1, line2], loc=1, prop={'size': 7})

# --- race preferred - green ---
ax = fig.add_subplot(4,3,3)
ax.set_title('race preferred')
ax.set_xticklabels(xlabels)

line1, = plt.plot(ticks, LR_race_paper, marker='d', markersize=4, linewidth=1, color='g', label='Results from [2]')
line2, = plt.plot(ticks, LR_race, marker='d', markersize=4, linewidth=1, color='black', label='Results in this paper')
plt.xticks(ticks, size=8)
plt.yticks(size=8)
plt.legend(handles=[line1, line2], loc=1, prop={'size': 7})

# ----- LINEAR SVC -----
# --- equal weights - red ---
ax = fig.add_subplot(4,3,4)
ax.set_xticklabels(xlabels)

plt.plot(ticks, LSVC_equal_paper, marker='o', markersize=4, linewidth=1, color='r')
plt.plot(ticks, LSVC, marker='o', markersize=4, linewidth=1, color='black')
plt.plot(ticks, LSVC_ARX, marker='o', markersize=4, linewidth=1, color='grey')
plt.ylabel('LINEAR SVC\n\nF1 score')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

# --- age preferred - blue ---
ax = fig.add_subplot(4,3,5)
ax.set_xticklabels(xlabels)

plt.plot(ticks, LSVC_age_paper, marker='v', markersize=4, linewidth=1, color='b')
plt.plot(ticks, LSVC_age, marker='v', markersize=4, linewidth=1, color='black')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

# --- race preferred - green ---
ax = fig.add_subplot(4,3,6)
ax.set_xticklabels(xlabels)

plt.plot(ticks, LSVC_race_paper, marker='d', markersize=4, linewidth=1, color='g')
plt.plot(ticks, LSVC_race, marker='d', markersize=4, linewidth=1, color='black')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

# ----- RANDOM FOREST -----
# --- equal weights - red ---
ax = fig.add_subplot(4,3,7)
ax.set_xticklabels(xlabels)

plt.plot(ticks, RF_equal_paper, marker='o', markersize=4, linewidth=1, color='r')
plt.plot(ticks, RF, marker='o', markersize=4, linewidth=1, color='black')
plt.plot(ticks, RF_ARX, marker='o', markersize=4, linewidth=1, color='grey')
plt.ylabel('RANDOM FOREST\n\nF1 score')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

# --- age preferred - blue ---
ax = fig.add_subplot(4,3,8)
ax.set_xticklabels(xlabels)

plt.plot(ticks, RF_age_paper, marker='v', markersize=4, linewidth=1, color='b')
plt.plot(ticks, RF_age, marker='v', markersize=4, linewidth=1, color='black')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

# --- race preferred - green ---
ax = fig.add_subplot(4,3,9)
ax.set_xticklabels(xlabels)

plt.plot(ticks, RF_race_paper, marker='d', markersize=4, linewidth=1, color='g')
plt.plot(ticks, RF_race, marker='d', markersize=4, linewidth=1, color='black')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

# ----- GRADIENT BOOSTING -----
# --- equal weights - red ---
ax = fig.add_subplot(4,3,10)
ax.set_xticklabels(xlabels)

plt.plot(ticks, GB_equal_paper, marker='o', markersize=4, linewidth=1, color='r')
plt.plot(ticks, GB, marker='o', markersize=4, linewidth=1, color='black')
plt.plot(ticks, GB_ARX, marker='o', markersize=4, linewidth=1, color='grey')
plt.ylabel('GRADIENT BOOSTING\n\nF1 score')
plt.xlabel('anonymization k-factor')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

# --- age preferred - blue ---
ax = fig.add_subplot(4,3,11)
ax.set_xticklabels(xlabels)

plt.plot(ticks, GB_age_paper, marker='v', markersize=4, linewidth=1, color='b')
plt.plot(ticks, GB_age, marker='v', markersize=4, linewidth=1, color='black')
plt.xlabel('anonymization k-factor')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

# --- race preferred - green ---
ax = fig.add_subplot(4,3,12)
ax.set_xticklabels(xlabels)

plt.plot(ticks, GB_race_paper, marker='d', markersize=4, linewidth=1, color='g')
plt.plot(ticks, GB_race, marker='d', markersize=4, linewidth=1, color='black')
plt.xlabel('anonymization k-factor')
plt.xticks(ticks, size=8)
plt.yticks(size=8)

plt.show()