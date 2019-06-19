import time
import config
from bs4 import BeautifulSoup
from pprint import pprint as pp
from selenium import webdriver


def remove_ns(string):
    new_string = ""
    for symbol in string:
        if symbol != "\n":
            new_string += symbol
    return new_string


def extract_review_data(parser):
    titles = [r.find("a").find("span").getText() for r in parser.findAll("div", {"class": "quote"})]
    texts = [remove_ns(r.find("p").getText()) for r in parser.findAll("div", {"class": "prw_rup prw_reviews_text_summary_hsx"})]
    res = []
    for i in range(len(titles)):
        d = {"title": titles[i],
             "text": texts[i]}
        res.append(d)
    return res


def get_reviews(url=config.URL):
    """ Collect reviews from a given tripadvisor restaurant page """
    driver = webdriver.Safari()
    driver.get(url)
    more_spans = driver.find_element_by_class_name("taLnk.ulBlueLinks")
    if more_spans:
        more_spans.click()
        time.sleep(1)
    print("Collecting data from page: {}\n".format(url))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    reviews_list = extract_review_data(soup)
    return reviews_list


if __name__ == "__main__":
    rev = get_reviews()
    pp(rev)
