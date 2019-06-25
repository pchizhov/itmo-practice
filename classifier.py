import json
import numpy as np
import pickle
from sklearn.feature_extraction.text import CountVectorizer

import config
from db import fill
from train.create_csv import get_clean_text
from train.train_model import train_model


def load_model(mp):
    with open(mp, 'rb') as lr_f:
        model_loaded = pickle.load(lr_f)
    return model_loaded


def prepare_data(clean_rs, voc):
    cv = CountVectorizer(binary=True, vocabulary=voc)
    return cv.fit_transform(clean_rs)


def get_categories(model, categories, x_data, row_data):
    pred = model.predict(x_data)
    proba = model.predict_proba(x_data)
    for i, p in enumerate(pred):
        indices = np.where(p)
        clear = True
        for e in proba[i]:
            if 0.100 < e < 0.900:
                clear = False
                break
        cats = [0, 0, 0, 0, 0]
        for idx in indices[0]:
            cats[int(idx)] = 1
        fill(row_data[i], cats[0], cats[1], cats[2], cats[3], cats[4], int(clear))
        if not clear:
            print('CATEGORIES: {}'.format(categories[indices]))
            print('PROBA: {}'.format(proba[i]))
            print('REVIEW: \n{}'.format(row_data[i]))


def classify():
    # train_model()
    model_path = config.MODEL_PATH
    categories = np.array(config.CATEGORY_WORDS)
    vocabulary_path = config.VOCABULARY_PATH
    reviews_texts_path = config.UNLABELED_REVIEWS_PATH

    with open(reviews_texts_path, 'r') as rt_f:
        reviews_text = [r["text"] for r in json.load(rt_f)]
    with open(vocabulary_path, 'r') as v_f:
        vocabulary = np.array(json.load(v_f))
    model = load_model(model_path)

    clean_reviews = get_clean_text(reviews_text)
    x_data = prepare_data(clean_reviews, vocabulary)
    get_categories(model, categories, x_data, reviews_text)
