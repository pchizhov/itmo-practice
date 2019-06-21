import time
from bs4 import BeautifulSoup
from selenium import webdriver


def remove_ns(string):
    new_string = ""
    for symbol in string:
        if symbol != "\n":
            new_string += symbol
    return new_string


def click_more(web_driver):
    more_spans = web_driver.find_element_by_class_name("taLnk.ulBlueLinks")
    if more_spans:
        more_spans.click()
        time.sleep(1)


def extract_reviews_data(parser):
    for div in parser.findAll("div", {"class": "mgrRspnInline"}):
        div.decompose()  # remove managers' responses
    texts = [remove_ns(r.find("p").getText()) for r in parser.findAll("div", {"class": "prw_rup prw_reviews_text_summary_hsx"})]
    return texts


def process_page(web_driver, page):
    web_driver.get(page)
    click_more(web_driver)
    print("Collecting data from page: {}\n".format(page))
    soup = BeautifulSoup(web_driver.page_source, "html.parser")
    return extract_reviews_data(soup)


def get_reviews(url):
    """ Collect reviews from a given tripadvisor restaurant page """
    # open the browser
    driver = webdriver.Safari()

    # get reviews from pages
    reviews_list = []
    while True:
        reviews_list.extend(process_page(driver, url))
        next_page = driver.find_elements_by_class_name("nav next taLnk ui_button primary")
        if next_page:
            url = next_page[0]
        else:
            break

    return reviews_list
