from db import Review, session
import config
import json


def make_dict(row):
    return {"text": row.text,
            "food": row.food,
            "service": row.service,
            "ambiance": row.ambiance,
            "price": row.price,
            "location": row.location}


def extract_reviews_from_db():
    s = session()
    labeled_revs = [make_dict(row) for row in s.query(Review).filter(Review.marked == 1).all()]
    unlabeled_revs = [make_dict(row) for row in s.query(Review).filter(Review.marked == 0).all()]
    return labeled_revs, unlabeled_revs


def load_reviews():
    lr, ur = extract_reviews_from_db()
    with open(config.LABELED_REVIEWS_PATH, "w") as lr_file:
        json.dump(lr, lr_file, ensure_ascii=False)
    with open(config.UNLABELED_REVIEWS_PATH, "w") as ur_file:
        json.dump(ur, ur_file, ensure_ascii=False)
