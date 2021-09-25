import math
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn

from utils.Comment import Comment


def calculate_word_average():
    index_names = df[df['Star Rating'] == 1].index

    total, words = 0, 0

    for i in index_names:
        text = df.iloc[i]["Review Text"]
        words += len(text.split())
        total += 1

    print("##### WORDS AVERAGE #####")
    print("Total words: ", words)
    print("Total one-star ratings: ", total)
    print("Average words per rating: ~", int(math.floor(words/total)))
    print("Real average words per rating: ", words/total)


def divide_data(percentage):
    aux = df.copy()
    total_test_data = int(len(aux) * percentage)
    aux = aux.sample(frac=1).reset_index(drop=True)
    return aux[:total_test_data], aux[total_test_data:]


def sanitize_data():
    df["titleSentiment"].fillna(0.5, inplace=True)
    df["titleSentiment"].replace("positive", 1.0, inplace=True)
    df["titleSentiment"].replace("negative", 0.0, inplace=True)


def get_closest_neighbors(train, other):
    distance_list = []
    columns = ["wordcount", "titleSentiment", "sentimentValue"]

    for i in range(len(train)):
        partial_sum = 0

        for attribute in columns:
            partial_sum += math.pow(train.iloc[i][attribute] - other[attribute], 2)

        comment = Comment(math.sqrt(partial_sum), train.iloc[i]["Star Rating"])
        distance_list.append(comment)

    return sorted(distance_list, key=lambda x: x.distance, reverse=False)[:k]


def classify(neighbours):
    class_dic = {}

    for neighbour in neighbours:
        if neighbour.rating in class_dic:
            class_dic[neighbour.rating] += 1
        else:
            class_dic[neighbour.rating] = 1

    return max(class_dic, key=class_dic.get)


def weighted_classify(neighbours):
    class_dic = {}
    zero_distance_dic = {}

    for neighbour in neighbours:
        if neighbour.distance == 0.0:
            if neighbour.rating in zero_distance_dic:
                zero_distance_dic[neighbour.rating] += 1
            else:
                zero_distance_dic[neighbour.rating] = 1
        else:
            if neighbour.rating in class_dic:
                class_dic[neighbour.rating] += 1/math.pow(neighbour.distance, 2)
            else:
                class_dic[neighbour.rating] = 1/math.pow(neighbour.distance, 2)

    if len(zero_distance_dic) > 0:
        return max(zero_distance_dic, key=zero_distance_dic.get)
    else:
        return max(class_dic, key=class_dic.get)


def knn(train, test, do_print):
    correctly_classified = 0
    total_classified = 0

    for i in range(len(test)):
        neighbours = get_closest_neighbors(train, test.iloc[i])
        classified_class = classify(neighbours)

        if test.iloc[i]["Star Rating"] == classified_class:
            correctly_classified += 1

        total_classified += 1

    if do_print:
        print("\n##### KNN #####")
        print("Well classified: ", correctly_classified)
        print("Total classified: ", total_classified)
        print("Precision: ", correctly_classified/total_classified, "\n")

    return correctly_classified, total_classified


def weighted_knn(train, test, do_print):
    correctly_classified = 0
    total_classified = 0

    for i in range(len(test)):
        neighbours = get_closest_neighbors(train, test.iloc[i])
        classified_class = weighted_classify(neighbours)

        if test.iloc[i]["Star Rating"] == classified_class:
            correctly_classified += 1

        total_classified += 1

    if do_print:
        print("##### WEIGHTED KNN #####")
        print("Well classified: ", correctly_classified)
        print("Total classified: ", total_classified)
        print("Precision: ", correctly_classified/total_classified, "\n")

    return correctly_classified, total_classified


# Las filas son la clasificacion real, las columnas la clasificación de knn
def get_confusion_matrix_knn(train, test):
    matrix = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

    for i in range(len(test)):
        neighbours = get_closest_neighbors(train, test.iloc[i])
        classified_class = classify(neighbours)
        real_class = test.iloc[i]["Star Rating"]
        matrix[real_class-1][classified_class-1] += 1

    print("##### KNN CONFUSION MATRIX #####")
    for elem in matrix:
        print(elem)

    return matrix


def get_confusion_matrix_weighted_knn(train, test):
    matrix = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

    for i in range(len(test)):
        neighbours = get_closest_neighbors(train, test.iloc[i])
        classified_class = weighted_classify(neighbours)
        real_class = test.iloc[i]["Star Rating"]
        matrix[real_class-1][classified_class-1] += 1

    print("\n##### KNN CONFUSION MATRIX #####")
    for elem in matrix:
        print(elem)

    return matrix


def cross_validation_knn():
    max_index = int(math.floor(len(df)/cross_validation_k))
    df_list = []

    for i in range(1, cross_validation_k+1):
        df_list.append(df[(i-1)*max_index:i*max_index])

    total_error = 0

    for j in range(cross_validation_k):
        send_df = df.drop(df_list[j].index)
        correct, total = knn(send_df, df_list[j], False)
        total_error += ((total-correct)/total)

    print("\n##### CROSS-VALIDATION KNN #####")
    print("Average error: ", total_error/cross_validation_k, "\n")
    return total_error / cross_validation_k


def cross_validation_weighted_knn():
    max_index = int(math.floor(len(df) / cross_validation_k))
    df_list = []

    for i in range(1, cross_validation_k + 1):
        df_list.append(df[(i - 1) * max_index:i * max_index])

    total_error = 0

    for j in range(cross_validation_k):
        send_df = df.drop(df_list[j].index)
        correct, total = weighted_knn(send_df, df_list[j], False)
        total_error += ((total-correct)/total)

    print("##### CROSS-VALIDATION WEIGHTED KNN #####")
    print("Average error: ", total_error / cross_validation_k, "\n")
    return total_error / cross_validation_k


def confusion_matrix(array):
    df_cm = pd.DataFrame(array, index=["1", "2", "3", "4", "5"],
                         columns=["1", "2", "3", "4", "5"])
    ax = plt.figure(figsize=(10, 7))
    sn.heatmap(df_cm, annot=True, cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Ground Truth")
    plt.show()


def draw_multiple_points(x_list, y_list):
    # Draw point based on above x, y axis values.
    plt.scatter(x_list, y_list, s=10)
    # Set chart title.
    plt.title("Cross-validation error given K")
    # Set x, y label text.
    plt.xlabel("K")
    plt.ylabel("Average error")
    plt.show()


k = 5
cross_validation_k = 5
df = pd.read_csv("resources/reviews_sentiment.csv", sep=";")
sanitize_data()
calculate_word_average()
train_data, test_data = divide_data(0.8)
knn(train_data, test_data, True)
weighted_knn(train_data, test_data, True)
get_confusion_matrix_knn(train_data, test_data)
get_confusion_matrix_weighted_knn(train_data, test_data)
cross_validation_knn()
cross_validation_weighted_knn()

# cross_validation_error = {}
# y = []
# x = []
#
# df = pd.read_csv("resources/reviews_sentiment.csv", sep=";")
# sanitize_data()
#
# for o in range(2, 7):
#     cross_validation_k = o
#     cross_validation_error[o] = 0
#
#     for u in range(5):
#         df = df.sample(frac=1).reset_index(drop=True)
#         cross_validation_error[o] += (cross_validation_knn()/5) # cross_validation_weighted_knn()
#
#     y.append(cross_validation_error[o])
#     x.append(o)
#
# draw_multiple_points(x, y)
