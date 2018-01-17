#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import sys
import os
from datetime import datetime
from random import randint


def get_move():
    sql = '''
    SELECT id, name, description, demo_url, times_served, date_last_served FROM daily_digest_exercise
    ORDER BY times_served
    LIMIT 1;
    '''
    conn = None
    data = ''
    
    try:
        # get the directory name for one level above current
        dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_file = os.path.join(dir_path, 'database/db.sqlite3')
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()

    except sqlite3.Error as e:
        print('move.get_move Error: {}'.format(e.args[0]))
        sys.exit(1)

    finally:
        if conn:
            conn.close()
            return data[0]


def update_times_served(move_id):
    conn = None
        
    try:
        dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_file = os.path.join(dir_path, 'database/db.sqlite3')
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute('''
        UPDATE daily_digest_exercise
        SET times_served=times_served+1
        WHERE id=(?);
        ''', (str(move_id),))
        conn.commit()
    
    except sqlite3.Error as e:
        print('move.update_times_served Error {}:'.format(e.args[0]))
        sys.exit(1)

    finally:
        if conn:
            conn.close()


def update_date_last_served(move_id):
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
        UPDATE daily_digest_exercise
        SET date_last_served=(?)
        WHERE id=(?);
        ''', (datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), str(move_id),))
        conn.commit()
    
    except sqlite3.Error as e:
        print('move.update_date_last_served Error {}:'.format(e.args[0]))
        sys.exit(1)

    finally:
        if conn:
            conn.close()

            
if __name__ == '__main__':
    exercise_id, name, description, video, times_served, date_last_served = get_move()
    print(exercise_id, name, times_served)
    # update_times_served(exercise_id)
    # update_date_last_served(exercise_id)
