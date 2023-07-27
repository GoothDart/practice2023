from pathlib import Path
import re
import os
import mysql.connector as mariadb
from mysql.connector import Error

def get_data():

    try:
        connection = mariadb.connect(user = 'Wslacklog_user', password = 'Wslacklog', database = 'Wslacklog_db', host = 'localhost', port = '3306')
        query = f"SELECT `id`, `file_name` FROM `file`"
        #print(query)
        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        id_file = cursor.fetchall()
        print(id_file)

        slerror = []
        sldate = []
        slslack = []
        slfile = []

        for idf in id_file:
            query = f"SELECT `error_detected` FROM `errors` WHERE `id_file` = {idf[0]}"
            cursor.execute(query)
            error_detected = cursor.fetchone()
            slerror.append(error_detected[0])
            #print(query)

            query = f"SELECT `start_date` FROM `dates` WHERE `id_file` = {idf[0]}"
            cursor.execute(query)
            start_date = cursor.fetchone()
            sldate.append(start_date[0])
            #print(query)

            query = f"SELECT `worst_slack` FROM `slacks` WHERE `id_file` = {idf[0]}"
            cursor.execute(query)
            worst_slack = cursor.fetchone()
            slslack.append(worst_slack[0])
            #print(query)

            slfile.append(idf[1])

        connection.close()
        #print('slerror: ', slerror)
        #print('sldate: ', sldate)
        #print('slslack: ', slslack)
        #print('slfile: ', slfile)

        print('<!doctype html>')
        print('<html>')
        print('<head>')
        print('<meta charset="utf-8">')
        print('<title>wslack</title>')
        print('</head>')
        print('<body>')
        print('<table border="1">')
        #print('<!--<caption></caption>-->')
        print('<tr>')
        print('<th>file_name</th>')
        print('<th>date</th>')
        print('<th>error</th>')
        print('<th>slack</th>')
        print('</tr>')
        for i in range(len(slfile)):
            print(f'<tr><td>{slfile[i]}</td><td>{sldate[i]}</td><td>{slerror[i]}</td><td>{slslack[i]}</td></tr>')
        print('</table>')
        print('</body>')

    except Error as error:
        print(f'Ошибка подключения к БД: {error}')
get_data()
