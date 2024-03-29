import json
import numpy as np
import pickle
from sklearn.feature_extraction.text import CountVectorizer

import config
from db import fill, load_reviews
from train.create_csv import get_clean_text


def load_model(mp):
    with open(mp, 'rb') as lr_f:
        model_loaded = pickle.load(lr_f)
    return model_loaded


def prepare_data(clean_rs, voc):
    cv = CountVectorizer(binary=True, vocabulary=voc)
    return cv.fit_transform(clean_rs)


def get_categories(model, x_data, row_data):
    pred = model.predict(x_data)
    proba = model.predict_proba(x_data)
    cnt = [0, 0]
    for i, p in enumerate(pred):
        indices = np.where(p)
        clear = True
        for e in proba[i]:
            if 0.050 < e < 0.800:
                clear = False
                break
        cats = [0, 0, 0, 0, 0]
        for idx in indices[0]:
            cats[int(idx)] = 1
        fill(row_data[i], cats[0], cats[1], cats[2], cats[3], cats[4], int(clear))
        cnt[int(clear)] += 1
    print("Reviews successfully classified with {} clear and {} confusing reviews\n".format(cnt[1], cnt[0]))


def classify():
    model_path = config.MODEL_PATH
    vocabulary_path = config.VOCABULARY_PATH

    reviews_texts = [r["text"] for r in load_reviews(labeled=False)]
    with open(vocabulary_path, 'r') as v_f:
        vocabulary = np.array(json.load(v_f))
    model = load_model(model_path)

    clean_reviews = get_clean_text(reviews_texts)
    x_data = prepare_data(clean_reviews, vocabulary)
    get_categories(model, x_data, reviews_texts)
