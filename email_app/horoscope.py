import os
import urllib.request
import json
import random
import pprint
import re

def get_mood():
    moods = ('thoughtful', 'happy', 'hysterical', 'concentrating', 'engaged',
             'demure', 'proud', 'lovestruck', 'hyper', 'bland', 'bored',
             'surprised', 'mischievious', 'shocked', 'innocent', 'meditative',
             'prudish', 'suspicious', 'guilty', 'anxious', 'interested',
             'curious')

    return random.choice(moods)


def get_keywords():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    words_file = os.path.join(dir_path, 'words.txt')

    with open(words_file, 'r') as text_file:
        words = text_file.readlines()

    keyword1 = random.choice(words).strip()
    keyword2 = random.choice(words).strip()

    if keyword1 and keyword2:
        return (keyword1, keyword2)

    else:
        return ('moxie', 'robot')
        
        
def theastrologer_api(zodiac):
    try:
        url = ('http://theastrologer-api.herokuapp.com/api/horoscope/'
               + zodiac + '/today')
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))

        data_dict = {}
        data_dict['horoscope'] = data['horoscope']
        data_dict['intensity'] = data['meta']['intensity']
        data_dict['keywords'] = data['meta']['keywords'].split(',')
        data_dict['mood'] = data['meta']['mood']
        data_dict['sunsign'] = data['sunsign']

    except urllib.error.URLError as e:
        ResponseData = e.read().decode('utf8', 'ignore')
        #print('horoscope.theastrologer_api:\n', ResponseData)
        data_dict = {}

    return data_dict


def horoscope_api(zodiac):
    try:
        time_interval = 'today'
        url = 'http://horoscope-api.herokuapp.com/horoscope/{0}/{1}'.format(
            time_interval, zodiac)

        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))

        data_dict = {}
        data_dict['horoscope'] = data['horoscope'][3:]
        data_dict['intensity'] = '{}%'.format(random.randint(30, 90))
        data_dict['keywords'] = get_keywords()
        data_dict['mood'] = get_mood()
        data_dict['sunsign'] = data['sunsign']

    except urllib.error.URLError as e:
        ResponseData = e.read().decode('utf8', 'ignore')
        #print('horoscope.horoscope_api:\n', ResponseData)
        data_dict = {}

    return data_dict


def findyourfate(zodiac):
    try:
        data_dict = {}
    
        url = ('http://www.findyourfate.com/rss/dailyhoroscope-feed.php?sign='
           + zodiac.title() + '&id=45')

        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')

        match = re.findall(r'<description>(.*)</description>', data)

        data_dict['horoscope'] = match[1]
        data_dict['intensity'] = '{}%'.format(random.randint(30, 90))
        data_dict['keywords'] = get_keywords()
        data_dict['mood'] = get_mood()
        data_dict['sunsign'] = zodiac
        
    except urllib.error.URLError as e:
        ResponseData = e.read().decode('utf8', 'ignore')
        #print('findyourfate:\n', ResponseData)
        data_dict = {}

    return data_dict


def get_horoscope(zodiac):

    data_dict = {}
    
    if zodiac not in ('aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
                      'libra', 'scorpio', 'sagittarius', 'capricorn',
                      'aquarius', 'pisces'):
        
        data_dict['horoscope'] = 'The robot has no idea what your sign is.'
        data_dict['intensity'] = '0%'
        data_dict['keywords'] = 'hidden from view'
        data_dict['mood'] = 'flat'
        data_dict['sunsign'] = 'Unknown'
        return data_dict

    else:
        try:
            data_dict = findyourfate(zodiac)
            if data_dict:
                return data_dict
            data_dict = theastrologer_api(zodiac)
            if data_dict:
                return data_dict
            data_dict = horoscope_api(zodiac)
            if data_dict:
                return data_dict

            data_dict['horoscope'] = 'The astrological forecast is too hazy today.  The robot is unable to make any predictions at this time.'
            data_dict['intensity'] = '50%'
            data_dict['keywords'] = 'initiative, volition'
            data_dict['mood'] = 'flat'
            data_dict['sunsign'] = zodiac

            return data_dict

        except urllib.error.URLError as e:
            ResponseData = e.read().decode('utf8', 'ignore')
            print(ResponseData)
            data_dict = {}
            data_dict['horoscope'] = 'The astrological forecast is too hazy today.  The robot is unable to make any predictions for you today.'
            data_dict['intensity'] = '50%'
            data_dict['keywords'] = 'initiative, volition'
            data_dict['mood'] = 'flat'
            data_dict['sunsign'] = zodiac

            return data_dict


if __name__ == '__main__':
    zodiac = ('aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra',
          'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces')
    data = get_horoscope(zodiac[4])
    #data = theastrologer_api(zodiac[0])
    pprint.pprint(data)
    #pprint.pprint(findyourfate(zodiac[0]))
