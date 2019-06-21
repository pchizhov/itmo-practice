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


def get_reviews(url):
    """ Collect reviews from a given tripadvisor restaurant page """
    # open the browser
    driver = webdriver.Safari()
    driver.get(url)

    # get reviews pages' urls
    pages = [url]
    page_nums = driver.find_elements_by_class_name("pageNumbers")
    if page_nums:
        pages = [a.get_attribute("href") for a in page_nums[0].find_elements_by_tag_name("a")]

    # get reviews from pages
    reviews_list = []
    for link in pages:
        driver.get(link)
        click_more(driver)
        print("Collecting data from page: {}\n".format(link))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        reviews_list.extend(extract_reviews_data(soup))

    return reviews_list
