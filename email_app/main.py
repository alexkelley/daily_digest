#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import datetime
import os
import pprint
from jinja2 import Environment, FileSystemLoader

from distribution_list import distribution_list
import entertainment
import earthporn
import send_from_mail
import trips
import weather
import quote
import horoscope
import move


# Run Code
start_time = time.time()

now = datetime.datetime.now()
date = datetime.datetime.strftime(now, '%Y-%m-%d')

angie_zip = trips.angie_location(date)
elizabeth_zip = trips.elizabeth_location(date)

# Build content that's relevant & consistent to all members
ep_text, ep_url = earthporn.get_image()

# [0]=id, [1]=quote, [2]=times_served, [3]=author, [4]=link
quote_data = quote.get_quote()

move_data = move.get_move()

(entertainment_article, entertainment_summary,
 entertainment_link, entertainment_image) = entertainment.get_eonline()

sports_title, sports_sub_title = entertainment.get_sports()
sports_link = 'http://espn.go.com/'

today = datetime.datetime.strftime(datetime.datetime.now(), '%B %-d, %Y')

email_data = {}
email_data['today'] = today

email_data['quote'] = quote_data[1]
email_data['quote_author'] = quote_data[3]
email_data['author_link'] = quote_data[4]

email_data['move_title'] = move_data[1]
email_data['move_description'] = move_data[2]
email_data['move_link'] = move_data[3]

email_data['entertainment_article'] = entertainment_article
email_data['entertainment_summary'] = entertainment_summary
email_data['entertainment_link'] = entertainment_link
email_data['entertainment_image'] = entertainment_image

email_data['sports_title'] = sports_title
email_data['sports_sub_title'] = sports_sub_title
email_data['sports_link'] = sports_link

email_data['picture_name'] = ep_text
email_data['picture_url'] = ep_url

# email_data['lolcat_url'] = earthporn.get_lolcats()

# Build data for each member of the distro
for value in distribution_list.values():

    name = value[0]
    email_data['name'] = name

    # get a traveller's location (Angie and EV so far)
    if name == 'Angie':
        location = angie_zip
    elif name == 'Elizabeth':
        location = elizabeth_zip
    else:
        location = value[2]

    # get the person's horoscope
    email_data['horoscope'] = horoscope.get_horoscope(value[1])

    try:
        weather_data = weather.load_data(location)
        city = weather_data['location']['name'].split(',', 1)[0]
        subject = '{0} digest for {1} in {2}'.format(today, name, city)
        email_data = weather.extract_weather_data(weather_data, email_data)

        # dir_path = os.path.dirname(os.path.abspath(__file__))
        # moon_image = os.path.join(dir_path,
        #                           'images/moon{}.gif'.format(
        #                               email_data['moon_phase_icon']))

        # weather_gauge_image = os.path.join(dir_path,
        #                                    'images/steampunk-weather-gauge.png')

        # sunrise_image = os.path.join(dir_path,
        #                                    'images/sunrise-512.png')

        # sunset_image = os.path.join(dir_path,
        #                                    'images/sunset-512.png')

        attachments = {
            # 'moon_image': moon_image,
            # 'steampunk_weather_gauge': weather_gauge_image,
            # 'sunrise': sunrise_image,
            # 'sunset': sunset_image
        }

        moon_image = 'http://www.moxie.ml/static/email_app/moon{}.gif'.format(
            email_data['moon_phase_icon'])
        email_data['moon_image'] = moon_image

        email_data['celsius'] = str(int(int(email_data['temperature']) - 32 * 5.0/9))
        
        env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
        template = env.get_template('email_body.html')
        message_body = template.render(data=email_data)

        send_from_mail.send_email("Alex's Robot <daily.digest2016@gmail.com>",
                                  value[3], subject, message_body, attachments)

    except AttributeError as a:
        print('AttributeError in main.py:', a)
    except KeyError as k:
        print('KeyError in main.py:', k)
    except:
        print('Unexpected error in main.py:')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])

    # filename = 'data/{}_{}.html'.format(name, date)
    # with open(filename, "wb") as fh:
    #     fh.write(bytes(message_body, 'UTF-8'))

# increment the quote times_served and date_last_served
quote.update_times_served(quote_data[0])
quote.update_date_last_served(quote_data[0])

# # increment the move times_served and date_last_served
move.update_times_served(move_data[0])
move.update_date_last_served(move_data[0])

# make_audio(summary)

print('The script ran in {:.2f} seconds'.format(time.time() - start_time))
