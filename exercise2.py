import pandas as pd


def calculate_exercise_one():
    index_names = df[df['Star Rating'] == 1].index

    total, words = 0, 0

    for i in index_names:
        words += df.iloc[i].wordcount
        total += 1

    print("Total words: ", words, "\n", "Total one-star ratings: ", total, "\n", "Average words per rating: ", words/total)


df = pd.read_csv("resources/reviews_sentiment.csv", sep=";")
calculate_exercise_one()