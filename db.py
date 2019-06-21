from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def fill(reviews):
    s = session()
    for r in reviews:
        review = Review(text=r,
                        food=0,
                        service=0,
                        ambiance=0,
                        price=0,
                        location=0,
                        marked=0)
        s.add(review)
    s.commit()


Base = declarative_base()
engine = create_engine("sqlite:///review.db")
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
