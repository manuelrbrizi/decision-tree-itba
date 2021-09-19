import pandas as pd
import math

from utils.Node import Node


# ver como calcular la entropia del atributo pero bien, porque aca no lo hacemos
def calculate_entropy():
    positive_cases = (df[df["Creditability"] == 1].count())[0]
    negative_cases = (df[df["Creditability"] == 0].count())[0]
    total_cases = positive_cases + negative_cases
    to_return = -(positive_cases / total_cases) * math.log2(positive_cases / total_cases) - (negative_cases / total_cases) * math.log2(negative_cases / total_cases)
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


def calculate_gain_given_attribute(attr):
    dic = {}

    for attr_value in df[attr].unique():
        dic[attr_value] = {}
        for column in df.columns:
            if column != "Creditability" and column != attr:
                dic[attr_value][column] = {}
                for column_value in df[column].unique():
                    dic[attr_value][column][column_value] = {}
                    dic[attr_value][column][column_value]["positive"] = 0
                    dic[attr_value][column][column_value]["negative"] = 0

    for i in range(len(df)):
        for j in range(1, len(df.columns)):
            if df.columns[j] != attr:
                for column_value in df[df.columns[j]].unique():
                    if df.iloc[i][0] == 1:
                        dic[df.iloc[i][attr]][df.columns[j]][column_value]["positive"] += 1
                    else:
                        dic[df.iloc[i][attr]][df.columns[j]][column_value]["negative"] += 1

    gain_dic = {}

    # attr_value = 1409, other_attr = hombre o mujer
    for attr_value in df[attr].unique():
        attr_entropy = calculate_entropy_of_attr(attr, attr_value)
        gain_dic[attr_value] = {}

        for other_attr in dic[attr_value].keys():
            other_attr_entropy = calculate_entropy_given_attr(dic, attr_value, other_attr)
            print("Attr ent = ", attr_entropy, ", Other ent = ", other_attr_entropy)
            gain_dic[attr_value][other_attr] = attr_entropy - calculate_entropy_given_attr(dic, attr_value, other_attr)

    return gain_dic


def calculate_entropy_of_attr(attr, attr_value):
    df_positive_cases = df[df["Creditability"] == 1]
    positive_cases = (df_positive_cases[df_positive_cases[attr] == attr_value].count())[0]

    df_negative_cases = df[df["Creditability"] == 0]
    negative_cases = (df_negative_cases[df_negative_cases[attr] == attr_value].count())[0]

    total_cases = positive_cases + negative_cases
    positive_cases /= total_cases
    negative_cases /= total_cases

    if positive_cases == 0.0 or negative_cases == 0.0:
        return 0
    else:
        return -positive_cases * math.log2(positive_cases) - negative_cases * math.log2(negative_cases)


def calculate_entropy_given_attr(dic, attr_value, other_attr):
    attr_entropy = 0
    total_cases = 0

    for other_attr_value in dic[attr_value][other_attr].keys():
        positive_cases = dic[attr_value][other_attr][other_attr_value]["positive"]
        negative_cases = dic[attr_value][other_attr][other_attr_value]["negative"]
        current_cases = (positive_cases + negative_cases)

        if current_cases != 0:
            total_cases += current_cases
            if positive_cases != 0:
                attr_entropy += current_cases*(positive_cases / current_cases)*math.log2((positive_cases/current_cases))
            if negative_cases != 0:
                attr_entropy += current_cases*(negative_cases/current_cases)*math.log2((negative_cases/current_cases))

    attr_entropy /= total_cases
    return attr_entropy


# todo cambiar este df, ya que estamos entrenando con todo el conjunto de datos
df = pd.read_csv("resources/german_credit.csv")
entropy, total_germans = calculate_entropy()
gain = calculate_gain()
parent_node = Node(max(gain, key=gain.get))
gain = calculate_gain_given_attribute(parent_node.name)
print(gain)
