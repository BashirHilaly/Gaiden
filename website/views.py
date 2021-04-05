from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Post, Comment, User, Figures
from . import db
from nltk.tokenize import sent_tokenize

import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# quote setup
import csv
import random

quote_index = 0

def random_line(fname, index):
    lines = open(fname, "r", encoding="utf-8").readlines()
    return lines[index]

views = Blueprint('views', __name__)


# Intro to Philosophy text
overview = open("website/authorized_written_content/intro/overview.txt", "r", encoding="utf-8").readlines()
origins = open("website/authorized_written_content/intro/origins.txt", "r", encoding="utf-8").readlines()
history = open("website/authorized_written_content/intro/history_intro.txt", "r", encoding="utf-8").readlines()


@views.route('/')
def home():
    # For random quote generation

    quote_index = random.randint(0, 24999)

    # TODO change this repo to this project's PATH
    quote = random_line('website/quote_library/quotes.csv', quote_index)
    author = random_line('website/quote_library/authors.csv', quote_index)

    return render_template("home.html",  user=current_user, quote=quote, quote_author=author)

@views.route('/intro')
def intro():
    return render_template("intro.html", user=current_user, overview=overview[0], origins=origins[0], history=history[0])

@views.route('/explore')
def explore():
    return render_template("explore.html", user=current_user)

@views.route('/forums', methods=['GET', 'POST'])
@login_required
def forums():
    if request.method == 'POST':
        post_title = request.form.get('postTitle')
        post_body = request.form.get('body')

        if len(post_title) <= 1:
            flash("Title too small.", category='error') 
        elif len(post_title) >= 150:
            flash("Title too large", category='error')
        elif len(post_body) <= 500:
            flash("Body too small.", category='error')
        elif len(post_body) >= 10000:
            flash("Body too large.", category='error')
        else:
            new_post = Post(title=post_title, content=post_body, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash("Posted!", category='success')

    return render_template("forums.html", user=current_user, Post=db.session.query(Post), Comment=db.session.query(Comment))


@views.route('/figures')
def figures():
    return render_template("figures.html", user=current_user, Figures=db.session.query(Figures))

@views.route('/figures/<person>')
def specific_figures(person):

    figure = Figures.query.filter_by(figure=person).first()
    text = figure.body
    body = sent_tokenize(text)

    paragraphs = [body[i * 10:(i + 1) * 10] for i in range((len(body) + 10 - 1) // 10 )]

    


    return render_template("figure.html", user=current_user, person=person, figure=figure, paragraphs=paragraphs)


@views.route('/timeline')
def timeline():


    """
    wikipedia = "https://en.wikipedia.org/wiki/List_of_philosophers_(I%E2%80%93Q)"
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
            try:
                table = driver.find_element_by_class_name('infobox')
                image = table.find_element_by_tag_name("img").get_attribute("src")
            except:
                image = "https://cdn-a.william-reed.com/var/wrbm_gb_food_pharma/storage/images/9/2/8/5/235829-6-eng-GB/Feed-Test-SIC-Feed-20142_news_large.jpg"
            body = []

            for p in paragraphs:
                body.append(p.text)


            figure = Figures(figure=title, image_address=image, body=''.join(body))
            db.session.add(figure)
            db.session.commit()

            print("Got info on " + title)

        print("Data Grabbed!")

        driver.quit()

    grabInfo(wikipedia)
    """



    return render_template('timeline.html', user=current_user)