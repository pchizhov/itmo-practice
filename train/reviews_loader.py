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


def extract_reviews_from_db(num):
    s = session()
    texts = [make_dict(row) for row in s.query(Review).filter(Review.marked == 1).all()[:num]]
    return texts


def load_reviews(num):
    revs = extract_reviews_from_db(num)
    f = open(config.reviews_texts_path, "w")
    json.dump(revs, f, ensure_ascii=False)
