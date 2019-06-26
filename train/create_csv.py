import re
import spacy
import json
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

import config
from db import load_reviews


alphabet = set(list("abcdefghijklmnopqrstuvwxyz"))


def punctuate(text):
    no_punctuation = re.compile("[.;:\-!\'’?,\"()&]")
    text = no_punctuation.sub(" ", text.lower())
    text = re.sub(r"\s+", " ", text)
    return text


def check_token(t):
    return not t.is_stop and len(t) > 1 and set(list(str(t))).issubset(alphabet)


def get_clean_text(reviews):
    reviews = [punctuate(r) for r in reviews]
    spacy_nlp = spacy.load('en_core_web_sm')
    clean_reviews = []
    for spacy_review in spacy_nlp.pipe(reviews, batch_size=100):
        clean_r = " ".join([token.lemma_ for token in spacy_review if check_token(token)])
        clean_reviews.append(clean_r)
    return np.array(clean_reviews)


def mark_labels(reviews):
    clean_reviews = get_clean_text([r["text"] for r in reviews])
    categories = np.array(config.CATEGORY_WORDS)
    labels = np.zeros((len(reviews), len(categories)))
    for i in range(len(reviews)):
        for cat, val in reviews[i].items():
            if cat != "text":
                labels[i][config.CATEGORY_WORDS.index(cat)] = val

    vec = CountVectorizer()
    x = vec.fit_transform(clean_reviews)
    with open(config.VOCABULARY_PATH, 'w') as rr_f:
        json.dump(vec.get_feature_names(), rr_f)

    df = pd.DataFrame(np.hstack((x.todense(), labels)),
                      columns=vec.get_feature_names() + ['y_' + s for s in categories.tolist()])
    return df


def wrap_in_csv():
    revs = np.array(load_reviews(labeled=True))
    df = mark_labels(revs)
    df.to_csv(config.CSV_PATH, index=False)
