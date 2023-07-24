from pathlib import Path
import re
import os
import mysql.connector as mariadb
from mysql.connector import Error

def get_data():

    try:
        connection = mariadb.connect(user = 'Wslacklog_user', password = 'Wslacklog', database = 'Wslacklog_db', host = 'localhost', port = '3306')
        query = f"SELECT `id`, `file_name` FROM `file`"
        print('!!!!!!!!!!!!')
        print(query)
        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        id_file = cursor.fetchall()

        slerror = []
        sldate = []
        slslack = []
        slfile = []

        for idf in id_file:
            query = f"SELECT `error_detected` FROM `errors` WHERE `id_file` = {idf[0]}"
            cursor.execute(query)
            error_detected = cursor.fetchone()
            slerror.append(error_detected)

            query = f"SELECT `start_date` FROM `dates` WHERE `id_file` = {idf[0]}"
            cursor.execute(query)
            start_date = cursor.fetchone()
            sldate.append(start_date)

            query = f"SELECT `worst_slack` FROM `slacks` WHERE `id_file` = {idf[0]}"
            cursor.execute(query)
            worst_slack = cursor.fetchone()
            slslack.append(worst_slack)

            slslack.append(idf[1])

        connection.close()
    except Error as error:
        print(f'Ошибка подключения к БД: {error}')
