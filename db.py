from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config


def fill(review, food=0, service=0, ambiance=0, price=0, location=0, marked=0):
    s = session()
    row = s.query(Review).filter(Review.text == review).one()
    if row:
        row.food = food
        row.service = service
        row.ambiance = ambiance
        row.price = price
        row.location = location
        row.marked = marked
    else:
        review = Review(text=review,
                        food=food,
                        service=service,
                        ambiance=ambiance,
                        price=price,
                        location=location,
                        marked=marked)
        s.add(review)
    s.commit()


Base = declarative_base()
engine = create_engine("sqlite:///" + config.DB_PATH)
session = sessionmaker(bind=engine)


class Review(Base):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    food = Column(Integer)
    service = Column(Integer)
    ambiance = Column(Integer)
    price = Column(Integer)
    location = Column(Integer)
    marked = Column(Integer)


Base.metadata.create_all(bind=engine)
