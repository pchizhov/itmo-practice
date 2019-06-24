import re
import spacy
import json
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

import config


def punctuate(text):
    no_punctuation = re.compile("[.;:\-!\'’?,\"()&]")
    text = no_punctuation.sub(" ", text.lower())
    text = re.sub(r"\s+", " ", text)
    return text


def get_clean_text(reviews):
    reviews = [punctuate(r) for r in reviews]
    spacy_nlp = spacy.load('en_core_web_sm')
    clean_reviews = []
    for spacy_review in spacy_nlp.pipe(reviews, batch_size=100):
        clean_r = " ".join([token.lemma_ for token in spacy_review if not token.is_stop and len(token) > 1])
        clean_reviews.append(clean_r)
    return np.array(clean_reviews)


def mark_labels(reviews):
    clean_reviews = get_clean_text([r["text"] for r in reviews])
    categories = np.array(config.category_words)
    labels = np.zeros((len(reviews), len(categories)))
    for i in range(len(reviews)):
        for cat, val in reviews[i].items():
            if cat != "text":
                labels[i][categories.index(cat)] = val

    # toDO TfidfVectorizer()
    vec = CountVectorizer(binary=True)
    x = vec.fit_transform(clean_reviews)

    df = pd.DataFrame(np.hstack((x.todense(), labels)),
                      columns=vec.get_feature_names() + ['y_' + s for s in categories.tolist()])
    return df


def wrap_in_csv():
    with open(config.reviews_texts_path, "r") as rev_file:
        revs = np.array(json.load(rev_file))
    df = mark_labels(revs)
    df.to_csv(config.labeled_reviews_path, index=False)
