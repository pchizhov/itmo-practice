from bottle import (
    route, run, template, request, redirect, get, post
)

from markup.tripadvisor import get_reviews
from db import Review, session, fill


@route("/")
def start():
    redirect("/reviews")


@route("/reviews")
def reviews_list():
    rows = s.query(Review).filter(Review.marked == 0).all()
    return template("reviews_template", rows=rows)


@route("/add_cat/")
def add_cat():
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
    row_id = request.query.id
    row = s.query(Review).filter(Review.id == row_id).one()
    row.marked = 1
    s.commit()
    redirect("/reviews")


@get("/new_restaurant")
def new_restaurant():
    return """<form action="/new_restaurant" method="post">
            Insert the TripAdvisor restaurant url: <input name="url" type="text" />
            <input value="Go!" type="submit" />
            </form>
            """


@post("/new_restaurant")
def collect():
    url = request.forms.get("url")
    fill(get_reviews(url))
    redirect("/reviews")


if __name__ == "__main__":
    s = session()
    run(host="localhost", port=8080)
