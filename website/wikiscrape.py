import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from . import db
from .models import Figures


wikipedia = "https://en.wikipedia.org/wiki/List_of_philosophers_(A%E2%80%93C)#A"
driver = webdriver.Chrome(ChromeDriverManager().install())


def grabInfo(site):
    driver.get(site)
    html_list = driver.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]/ul[3]')
    list_of_philosophers = html_list.find_elements_by_tag_name("li")
    i = 0
    window_index = 0
    for p in list_of_philosophers:
        i += 1
        link = p.find_element_by_tag_name('a')
        ActionChains(driver).key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
    for tab in range(i):
        window_index += 1
        driver.switch_to.window(driver.window_handles[window_index])
        title = driver.find_element_by_tag_name("h1").text
        paragraphs = driver.find_elements_by_tag_name("p")
        table = driver.find_element_by_class_name('infobox')
        image = table.find_element_by_tag_name("img").get_attribute("src")
        body = []

        for p in paragraphs:
            body.append(p.text)


        figure = Figures(figure=title, image_address=image, body=''.join(body))
        db.session.add(figure)
        db.session.commit()

        ActionChains(driver).key_down(Keys.CONTROL).send_keys('w').key_up(Keys.CONTROL).perform()

        print("Data Grabbed!")




grabInfo(wikipedia)