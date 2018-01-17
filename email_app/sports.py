#! /usr/bin/env python3

import feedparser
import html.parser
import re

from urllib.request import urlopen
import datetime
import json
import codecs


url = 'http://api.cbssports.com/fantasy/sports/baseball'
response = urlopen(url).readall().decode('utf-8')
print(response)
#reader = codecs.getreader(response.headers.get_content_charset())
#data = json.load(response)
#blockchain = float(data.get('USD').get('last'))
#print(data)
