#! /usr/bin/env python3

import wget

url = 'https://www.wunderground.com/graphics/moonpictsnew/moon{}.gif'

for i in range(40):
    try:
        wget.download(url.format(i))
    except:
        print('Bad URL')
