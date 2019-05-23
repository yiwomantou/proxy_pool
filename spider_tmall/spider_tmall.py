from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from datetime import datetime

KEYWORD = "iPad"
MAX_PAGE = 80

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
url = "https://list.tmall.com/search_product.htm?q={}".format(KEYWORD)
browser.get(url)


def save_txt(data):
    with open(file="天猫_{}.txt".format(KEYWORD), mode="a", encoding="utf-8") as f:
        f.write(str(data) + "\n")


def get_products():
    html = browser.page_source
    doc = pq(html, parser='html')
    items = doc(".product-iWrap").items()
    for item in items:
        try:
            s = []
            for index, span in enumerate(item.find(".productStatus span").items()):
                s.append(span)
            month_deal_num = s[0].find("em").text()
            collect_num = s[1].find("a").text()
        except:
            month_deal_num = 0
            collect_num = 0

        product = {
            "product_url": item.find(".productImg-wrap a").attr("href"),
            "img": item.find(".productImg-wrap a img").attr("src"),
            "price": item.find(".productPrice em").attr("title"),
            "title": item.find(".productTitle a").attr("title"),
            "shop": item.find(".productShop a").text(),
            "month_deal_num": month_deal_num,
            "collect_num": collect_num,
        }
        print(product)
        save_txt(product)


def index_page(page):
    print("正在爬取第{}页".format(page))
    try:
        if page > 1:
            jump = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.ui-page-skipTo")))
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ui-btn-s")))
            jump.clear()
            jump.send_keys(page)
            submit.click()
        wait.until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "input.ui-page-skipTo"), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-iWrap")))
        get_products()
    except TimeoutException:
        index_page(page)


def main():
    for i in range(1, MAX_PAGE + 1):
        index_page(i)
        break


if __name__ == "__main__":
    main()
    with open(file="天猫_{}.txt".format(KEYWORD), mode="a", encoding="utf-8") as f:
        f.write("----------------------------------------" + str(datetime.now()) + "\n")
