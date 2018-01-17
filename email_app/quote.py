#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import sys
import os
from datetime import datetime
from random import randint


def get_quote():
    sql1 = '''
    SELECT daily_digest_quote.id, quote_text, times_served, author, biography_url
    FROM daily_digest_quote
    INNER JOIN daily_digest_quote_author ON daily_digest_quote.quote_author_id_id = daily_digest_quote_author.id
    WHERE times_served = 0
    ORDER BY times_served
    LIMIT 1;
    '''

    sql2 = '''
    SELECT daily_digest_quote.id, quote_text, times_served, author, biography_url
    FROM daily_digest_quote
    INNER JOIN daily_digest_quote_author ON daily_digest_quote.quote_author_id_id = daily_digest_quote_author.id
    WHERE date_last_served < date(date('now'), '-5 months')
    ORDER BY times_served
    LIMIT 20;
    '''
    conn = None
    data = ''
    
    try:
        # get the directory name for one level above current
        dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_file = os.path.join(dir_path, 'database/db.sqlite3')
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql1)
        data = cur.fetchall()
        if data:
            return data[0]
        else:
            cur.execute(sql2)
            data = cur.fetchall()
            quote_index = randint(0, len(data)-1)
            return data[quote_index]


    except sqlite3.Error as e:
        print('quote.get_quote Error: {}'.format(e.args[0]))
        sys.exit(1)

    finally:
        if conn:
            conn.close()


def update_times_served(quote_id):
    conn = None
        
    try:
        dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_file = os.path.join(dir_path, 'database/db.sqlite3')
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute('''
        UPDATE daily_digest_quote
        SET times_served=times_served+1
        WHERE id=(?);
        ''', (str(quote_id),))
        conn.commit()
    
    except sqlite3.Error as e:
        print('quote.update_times_served Error {}:'.format(e.args[0]))
        sys.exit(1)

    finally:
        if conn:
            conn.close()


def update_date_last_served(quote_id):
    '''
    2016-09-07 21:46:29
    '''
    conn = None
        
    try:
        dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_file = os.path.join(dir_path, 'database/db.sqlite3')
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute('''
        UPDATE daily_digest_quote
        SET date_last_served=(?)
        WHERE id=(?);
        ''', (datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), str(quote_id),))
        conn.commit()
    
    except sqlite3.Error as e:
        print('quote.update_date_last_served Error {}:'.format(e.args[0]))
        sys.exit(1)

    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    print(get_quote())
