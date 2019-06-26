from bottle import (
    route, run, template, request, redirect, get, post
)

from markup.tripadvisor import get_reviews
from train.train_model import train_model
from classifier import classify
from db import Review, session, fill


@route("/")
def start():
    redirect("/reviews")


@route("/reviews")
def reviews_list():
    s = session()
    rows = s.query(Review).filter(Review.marked == 0).all()
    return template("markup/reviews_template", rows=rows)


@route("/add_cat/")
def add_cat():
    s = session()
    cat = str(request.query.cat)
    row_id = request.query.id
    row = s.query(Review).filter(Review.id == row_id).one()
    if cat == "food":
        row.food += 1
        row.food %= 2
    elif cat == "service":
        row.service += 1
        row.service %= 2
    elif cat == "ambiance":
        row.ambiance += 1
        row.ambiance %= 2
    elif cat == "price":
        row.price += 1
        row.price %= 2
    elif cat == "location":
        row.location += 1
        row.location %= 2
    s.commit()
    redirect("/reviews")


@route("/update/")
def update():
    s = session()
    row_id = request.query.id
    row = s.query(Review).filter(Review.id == row_id).one()
    row.marked = 1
    s.commit()
    redirect("/reviews")


@get("/new_restaurant")
def new_restaurant():
    return """
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <div class="ui container" style="padding-top: 10px;">
    <form action="/new_restaurant" method="post">
            Insert the TripAdvisor restaurant url: <input name="url" type="text" />
            <input class="ui bottom floated small primary button" value="Go!" type="submit" />
            </form>
            </div>
            """


@post("/new_restaurant")
def collect():
    url = request.forms.get("url")
    for r in get_reviews(url):
        fill(r)
    redirect("/reviews")


@route("/predict")
def predict():
    classify()
    redirect("/reviews")


@route("/train")
def train():
    f1_score = train_model()
    print("Model successfully trained with score: {}\n".format(f1_score))
    redirect("/reviews")


def load():
    run(host="localhost", port=8080)
