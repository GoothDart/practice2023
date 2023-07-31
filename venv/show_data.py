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

        slfile = []
        for idf in id_file:
            slfile.append(idf[1])
        slchecked_idfile = []

        if _POST:
            date_need = _POST['date_need']
            error_show = _POST['error_show']
            for idf in id_file:
                if _POST[f'{idf[1]}']:
                    slchecked_idfile.append(idf)
            date_from = _POST['date_from']
            date_to = _POST['date_to']
        else:
            date_need = False
            error_show = 'All'
            slchecked_idfile = id_file

        slerror = []
        sldate = []
        slslack = []
        slchec_file = []

        for idf in slchecked_idfile:

            fl_err = 0
            query = f"SELECT `error_detected` FROM `errors` WHERE `id_file` = {idf[0]}"
            cursor.execute(query)
            error_detected = cursor.fetchone()
            if error_show == 'All':
                fl_err = 1
                #slerror.append(error_detected[0])
            elif error_show == 'With an error':
                if error_detected == True:
                    fl_err = 1
                    #slerror.append(error_detected[0])
                else:
                    continue
            elif error_show == 'Without an error':
                if error_detected == False:
                    fl_err = 1
                    #slerror.append(error_detected[0])
                else:
                    continue
            #print(query)

            fl_dt = 0
            query = f"SELECT `start_date` FROM `dates` WHERE `id_file` = {idf[0]}"
            cursor.execute(query)
            start_date = cursor.fetchone()
            if date_need:
                if (date_from <= start_date[0]) and (date_to >= start_date[0]):
                    fl_dt = 1
                    #sldate.append(start_date[0])
                else:
                    continue
            else:
                fl_dt = 1
                #sldate.append(start_date[0])
            #print(query)

            query = f"SELECT `worst_slack` FROM `slacks` WHERE `id_file` = {idf[0]}"
            cursor.execute(query)
            worst_slack = cursor.fetchone()
            if (fl_err == 1) and (fl_dt == 1):
                slerror.append(error_detected[0])
                sldate.append(start_date[0])
                slslack.append(worst_slack[0])
                slchec_file.append(idf[1])
            else:
                continue
            #print(query)

            #slchec_file.append(idf[1])

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
        print('<form action = "/cgi-bin/show_data.py" method = "post">')

        print('< input type = "checkbox" name = "date_need">does date need? </input></br>')
        print('<div>from: < input type = "text" name = "date_from" > </div>')
        print('<div>to: < input type = "text" name = "date_to" ></div><br>')

        print(' < select name = "error_show" >')
        print('<option value= "All" selected>All</option>')
        print('<option value= "With an error">With an error</option>')
        print('<option value= "Without an error">Without an error</option>')
        print('</select></br>')

        for file_name in slfile:
            print(f'<input type= "checkbox" name= "{file_name}" checked>{file_name}</input></br>')

        print('<input type = "submit" value = "Submit"/>')
        print('</form>')

        print('<table border="1">')
        #print('<!--<caption></caption>-->')
        print('<tr>')
        print('<th>file_name</th>')
        print('<th>date</th>')
        print('<th>error</th>')
        print('<th>slack</th>')
        print('</tr>')
        for i in range(len(slchec_file)):
            print(f'<tr><td>{slchec_file[i]}</td><td>{sldate[i]}</td><td>{slerror[i]}</td><td>{slslack[i]}</td></tr>')
        print('</table>')
        print('</body>')

    except Error as error:
        print(f'Ошибка подключения к БД: {error}')
get_data()

