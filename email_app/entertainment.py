#! /usr/bin/env python3

import feedparser
import html.parser
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from lxml import etree


def clean_up_title(text):
    '''
    Take a text string from TMZ headlines

    Return a human readable text string
    '''
    h = html.parser.HTMLParser(convert_charrefs=True)

    m = re.match(r'^(.*)&hellip', text)

    clean_title = m.group(1)
    clean_title = html.unescape(clean_title)

    if ']]' in clean_title:
        return clean_title[clean_title.find(']] ')+3:]

    return clean_title


def get_headline():
    '''
    Return a headline and url from TMZ
    '''
    tmz_feed_url = 'http://www.tmz.com/category/gossip-rumors/rss.xml'

    feed = feedparser.parse(tmz_feed_url)

    articles = []

    for i in range(len(feed)):
        raw_title = feed['items'][i]['summary_detail']['value']
        link = feed['items'][i]['links'][0]['href']
        try:
            if raw_title:
                articles.append((clean_up_title(raw_title), link))
        except AttributeError as e:
            print("Regex in `entertainment.py` failed to clean up title of a TMZ article:\n", e)

    return articles


def get_top_story():
    tmz_url = 'http://www.tmz.com/'
    html_data = urlopen(tmz_url)
    soup = BeautifulSoup(html_data, 'html.parser')

    title = []
    for x in soup.select('h1')[0]:
        try:
            if x.name == 'span':
                title.append(x.get_text())
        except:
            pass

    return title


def get_sports():
    espn_url = 'http://espn.go.com/'
    html_data = urlopen(espn_url)
    soup = BeautifulSoup(html_data, 'html.parser')

    # title = ''
    # for x in soup.select('h1')[0]:
    #     try:
    #         if x.name == 'span':
    #             title += x.get_text() + ' '
    #     except:
    #         pass

    title = soup.select('h1')[1].get_text()
    sub_title = soup.select('p')[1].get_text()

    return (title, sub_title)


def get_people():
    url = 'http://feeds.people.com/people/headlines'
    feed = feedparser.parse(url)

    item = feed['items'][0]
    title = item['title']
    summary = item['summary']
    link = item['link']
    image = item['media_thumbnail']

    return (title, summary, link, image)


def get_time():
    url = 'http://feeds2.feedburner.com/time/entertainment'

    time = feedparser.parse(url)

    title = time['entries'][0]['title']
    summary = time['entries'][0]['description']
    link = time['entries'][0]['link']
    image = time['entries'][0]['media_thumbnail']
    
    return (title, summary, link, image)


def get_animal():
    url = 'http://feeds.feedburner.com/ICanHasCheezburger'
    feed = feedparser.parse(url)

    item = feed['items'][0]
    title = item['title']
    summary = item['summary']
    link = item['link']

    return (title, summary, link)

def get_eonline():
    url = 'http://syndication.eonline.com/syndication/feeds/rssfeeds/topstories.xml'
    feed = feedparser.parse(url)

    item = feed['items'][0]
    title = item['title']
    summary = item['description']
    link = item['link']
    image = '#' #item['media_thumbnail']

    return (title, summary, link, image)    

if __name__ == '__main__':
    feed_data = get_eonline()
    for i in range(len(feed_data)):
        print(feed_data[i])
