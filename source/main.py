# -*- coding: utf-8 -*-

import urllib
import time
from lxml.html import fromstring
import sqlalchemy
from sqlalchemy import Column, Integer, String

engine = sqlalchemy.create_engine("mysql://root@localhost/parser")

def getArticles(url):
    articles = []

    html = urllib.urlopen(url).read();

    page = fromstring(html)

    page.make_links_absolute(url)


    for link in page.cssselect('.post-title a'):
        articles.append(getArticle(link.attrib['href']))
        print "sleeping after article parse"
        time.sleep(2)

    return articles


def getArticle(url):
    html = urllib.urlopen(url).read()
    page = fromstring(html)
    page.make_links_absolute(url)

    text = page.cssselect('.article-entry.text')[0].text_content().encode('utf-8', 'ignore')

    engine.execute(
        sqlalchemy.text("insert lingvo_article (article, url) values (:article, :url)"),
        article=text,
        url=url
    )

url = 'http://techcrunch.com/page/%s/'

articles = []
for x in range(11, 100):
    articles = articles + getArticles(url % x)
    print ('%s pages parsed' % x)

print ('parsed %s articles' % len(articles))