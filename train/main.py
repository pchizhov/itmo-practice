import pandas as pd
import pickle
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

import config
from train.reviews_loader import load_reviews
from train.create_csv import wrap_in_csv


def train_classifier(x, y):
    c = OneVsRestClassifier(LogisticRegression(solver='sag'), n_jobs=-1)
    c.fit(x, y)
    return c


def evaluate_classifier(c, x_test, y_test):
    predictions = c.predict(x_test)
    return f1_score(y_test, predictions, average='weighted')


def save_model(model, file_path):
    with open(file_path, 'wb') as lr_f:
        pickle.dump(model, lr_f)


if __name__ == "__main__":
    # load_reviews(1000)
    # wrap_in_csv()
    df = pd.read_csv(config.labeled_reviews_path)
    columns = df.columns

    train_d, test_d = train_test_split(df, test_size=0.2)

    x_columns = [c for c in columns if 'y_' not in c]
    y_columns = [c for c in columns if 'y_' in c]

    classifier = train_classifier(train_d[x_columns], train_d[y_columns])
    print(evaluate_classifier(classifier, test_d[x_columns], test_d[y_columns]))

    logistic_regression_path = 'lr_model.sav'
    save_model(classifier, logistic_regression_path)
