#!/usr/bin/env python3
from pathlib import Path
import re
import os
import mysql.connector as mariadb
from mysql.connector import Error
import cgi
import cgitb
from datetime import datetime as dt

#cgitb.enable(display=0, logdir='/var/www/cgi-bin')
#cgitb.enable()
#cgitb.handler()

#фонкция обработки строки с датой из типа str в тип datetime
def date_normalization(date):
    date = date.split()
    normdate = ['0001', '1', '1', '00:00:00']
    slmounths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    for pd in date:
        if ':' in pd:
            normdate[3] = pd

        elif re.search(r'\b\d{2}$', pd):
            normdate[2] = pd

        elif re.search(r'\d{4}', pd):
            normdate[0] = pd

        elif pd in slmounths:
            for i in range(len(slmounths)):
                if pd == slmounths[i]:
                    normdate[1] = str(i + 1)

    #vrdat = normdate[0:3]
    #datet = ' '.join(vrdat)
    dtv3 = ' '.join(normdate)

    return dt.strptime(dtv3, "%Y %m %d %X")

#основной код, берет информацию из бд и выводит ее на экран
def get_data():

    #подключение к базе и операции с массивом имен и id файлов
    try:
        connection = mariadb.connect(user = 'Wslacklog_user', password = 'Wslacklog', database = 'Wslacklog_db', host = 'localhost', port = '3306')
        query = f"SELECT `id`, `file_name` FROM `file`"
        #print(query)
        cursor = connection.cursor(buffered=True)
        cursor.execute(query)
        id_file = cursor.fetchall()
        #print(id_file)

        slfile = []
        for idf in id_file:
            slfile.append(idf[1])
        slchecked_idfile = []

        #получение информации из масива post
        form = cgi.FieldStorage()
        #cgitb.enable()
        cgitb.enable(display=0, logdir='/var/www/cgi-bin')

        if form:
            try:
                print("Content-Type: text/html;charset=utf-8")
                print ("Content-type:text/html\r\n")
                date_need = form['date_need'].value
                if date_need == 'date need':
                    date_need = True
                else:
                    date_need = False
                error_show = form['error_show'].value
                all_files = form['all_files'].value
                if all_files == 'all files':
                    all_files = True
                else:
                    all_files = False
                form_keys = form.keys()
                if all_files == True:
                    slchecked_idfile = id_file
                else:
                    for idf in id_file:
                        if idf[1] in form_keys:
                            slchecked_idfile.append(idf)
                        else:
                            continue
                date_from = form['date_from'].value
                date_from = dt.strptime(date_from, "%Y %m %d %X")
                date_to = form['date_to'].value
                date_to = dt.strptime(date_to, "%Y %m %d %X")
            except KeyError:
                #date_need = False
                #error_show = 'All'
                #all_files = True
                #slchecked_idfile = id_file

                exs_useless = 101
                #otlad_post = form.keys()
                #print("Content-Type: text/html;charset=utf-8")
                #print ("Content-type:text/html\r\n")
                #for k in otlad_post:
                    #v = form[k]
                    #print(f'<div>{k} - {v}</div></br>')
        else:
            date_need = False
            error_show = 'All'
            all_files = True
            slchecked_idfile = id_file
            
        #cgitb.enable()
        cgitb.enable(display=0, logdir='/var/www/cgi-bin')

        slerror = []
        sldate = []
        slslack = []
        slchec_file = []

        #достаем нужные данные из базы данных
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

            fl_dt = 0
            query = f"SELECT `start_date` FROM `dates` WHERE `id_file` = {idf[0]}"
            cursor.execute(query)
            start_date = cursor.fetchone()
            start_date = date_normalization(start_date[0])
            if date_need:
                if (date_from <= start_date) and (date_to >= start_date):
                    fl_dt = 1
                    #sldate.append(start_date[0])
                else:
                    continue
            else:
                fl_dt = 1
                #sldate.append(start_date[0])

            query = f"SELECT `worst_slack` FROM `slacks` WHERE `id_file` = {idf[0]}"
            cursor.execute(query)
            worst_slack = cursor.fetchone()
            if (fl_err == 1) and (fl_dt == 1):
                slerror.append(error_detected[0])
                sldate.append(start_date)
                if worst_slack[0]:
                    slslack.append(worst_slack[0])
                else:
                    slslack.append(-1)
                slchec_file.append(idf[1])
            else:
                continue

            #slchec_file.append(idf[1])

        connection.close()
        #выводим форму для сортировки данных и сами данные

        #print("Content-Type: text/html;charset=utf-8")
        #print ("Content-type:text/html\r\n")

        print('<form action = "/cgi-bin/show_data3.py" method = "post">')

        #print('<input type = "checkbox" name = "date_need">does date need?</input></br>')
        print(' <select name = "date_need">')
        print('<option value= "date does not need" selected>date does not need</option>')
        print('<option value= "date need">date need</option>')
        print('</select></br>')
        print('<div>enter the date in the following format separated by a space: 0000(year) 0(month) 0(day) 00:00:00(hms)</div></br>')
        print('<div>from: <input type = "text" name = "date_from" required value= "0002 1 1 00:00:00"></div>')
        print('<div>to: <input type = "text" name = "date_to" required value= "2999 1 1 00:00:00"></div><br>')

        print(' <select name = "error_show">')
        print('<option value= "All" selected>All</option>')
        print('<option value= "With an error">With an error</option>')
        print('<option value= "Without an error">Without an error</option>')
        print('</select></br>')

        #print('<input type = "checkbox" name = "all_files" checked>choose all files?</input></br>')
        print(' <select name = "all_files">')
        print('<option value= "all files" selected>all files</option>')
        print('<option value= "not all files">not all files</option>')
        print('</select></br>')
        print('<div>list of files:</div></br>')
        for file_name in slfile:
            print(f'<input type= "checkbox" name= "{file_name}">{file_name}</input></br>')

        print('<input type = "submit" value = "Submit"/>')
        print('</form>')

        print('<table border="1">')
        print('<tr>')
        print('<th>file_name</th>')
        print('<th>date</th>')
        print('<th>error</th>')
        print('<th>slack</th>')
        print('</tr>')

        if date_need:
            for i in range(len(slchec_file)-1):
                minid = i
                g = i + 1
                while g < len(slchec_file):
                    if sldate[minid] > sldate[g]:
                        minid = g
                    g = g + 1
                if minid != i:
                    vsp_d = sldate[minid]
                    vsp_f = slchec_file[minid]
                    vsp_e = slerror[minid]
                    vsp_s = slslack[minid]

                    sldate[minid] = sldate[i]
                    slchec_file[minid] = slchec_file[i]
                    slerror[minid] = slerror[i]
                    slslack[minid] = slslack[i]
                    
                    sldate[i] = vsp_d
                    slchec_file[i] = vsp_f
                    slerror[i] = vsp_e
                    slslack[i] = vsp_s

        for i in range(len(slchec_file)):
            print(f'<tr><td>{slchec_file[i]}</td><td>{sldate[i]}</td><td>{slerror[i]}</td><td>{slslack[i]}</td></tr>')
        print('</table>')

    except Error as error:
        print(f'Ошибка подключения к БД: {error}')
get_data()

