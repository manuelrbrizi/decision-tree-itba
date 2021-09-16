import pandas as pd
import math


def calculate_entropy():
    positive_cases = (df[df["Creditability"] == 1].count())[0]
    negative_cases = (df[df["Creditability"] == 0].count())[0]
    total_cases = positive_cases + negative_cases
    to_return = -(positive_cases / total_cases) * math.log2(positive_cases / total_cases) \
                - (negative_cases / total_cases) * math.log2(negative_cases / total_cases)
    print("Positive cases: ", positive_cases, "\nNegative cases: ", negative_cases, "\nEntropy: ", to_return)
    return to_return, total_cases


def calculate_gain():
    dic = {}

    for column in df.columns:
        if column != "Creditability":
            dic[column] = {}
            for val_type in df[column].unique():
                dic[column][val_type] = {}
                dic[column][val_type]["positive"] = 0
                dic[column][val_type]["negative"] = 0

    for i in range(len(df)):
        for j in range(1, len(df.columns)):
            if df.iloc[i][0] == 1:
                dic[df.columns[j]][df.iloc[i][j]]["positive"] += 1
            else:
                dic[df.columns[j]][df.iloc[i][j]]["negative"] += 1

    gain_dic = {}

    for column in df.columns:
        if column != "Creditability":
            gain_dic[column] = entropy
            for val_type in dic[column].keys():
                att_entropy, att_cases = calculate_attribute_entropy(dic, column, val_type)
                gain_dic[column] -= (att_cases/total_germans)*att_entropy

    return gain_dic


def calculate_attribute_entropy(dic, column, val_type):
    positive_cases = dic[column][val_type]["positive"]
    negative_cases = dic[column][val_type]["negative"]
    total_cases = positive_cases + negative_cases
    positive_cases /= total_cases
    negative_cases /= total_cases

    if positive_cases == 0.0 or negative_cases == 0.0:
        return 0, total_cases
    else:
        return -positive_cases * math.log2(positive_cases) - negative_cases * math.log2(negative_cases), total_cases


df = pd.read_csv("resources/german_credit.csv")
entropy, total_germans = calculate_entropy()
gain = calculate_gain()
print(gain)
