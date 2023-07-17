from pathlib import Path
import re
import os

#поиск ошибки
def searcherror(line):
    if ('ERROR' in line) or ('FATAL' in line):
        span = re.search(r'(ERROR)|(FATAL)', line).span()
        if span[0] == 0:
            return True
        else:
            return False

#поиск slack
#if re.search(r'([Rr]eport [Ss]lack)|(Initial slew slack)', line):
def searchworstslack(line):
    if re.search(r'[Ww]orst [Ss]lack', line):
        span = re.search(r'[Ww]orst [Ss]lack', line).span()
        line = line[span[1]:]
        line = line.split()
        for elem in line:
            if re.search(r'\d', elem):
                return elem

 #ищет время и выдает срез строки после найденных слов и когда появляется первая буква\цифра. span - кортеж из начала и конца найденного соответствия(индексы)
def searchdate(line, flagdate):
    if flagdate:
        return [line, False]
    elif re.search(r'(\b[dD]ate)|([Ss]tart [tT]ime)', line):
        span = re.search(r'(\b[dD]ate)|([Ss]tart [tT]ime)', line).span()
        line = line[span[1]:]
        span = re.search(r'\w', line)
        if span:
            span = span.span()
            line = line[span[0]:]
            date = line
            return [line, flagdate]
        else:
            return ['', True]
    else: return ['', flagdate]

def main():
    namedir = input('введите имя папки')
    listlog = os.listdir(namedir)
    for logpath in listlog:

        if Path(logpath).suffix != '.log':
            continue

        fldict = dict()
    
        flagerror = False
        logpath = namedir + '/' + logpath
        log = open(logpath)
        path = Path(logpath)
        slack = []
        date_fldate = ['', False]
        date = ''

        for line in log:

            line = line.strip()
        
            #поиск ошибки
            if searcherror(line):
                flagerror = True

            #ищет время и выдает срез строки после найденных слов и когда появляется первая буква\цифра. span - кортеж из начала и конца найденного соответствия(индексы)
            date_fldate = searchdate(line, date_fldate[1])
            if date_fldate[0]:
                date = date_fldate[0]

            #поиск slack
            if searchworstslack(line):
                slack.append(searchworstslack(line))

        fldict['Filename'] = path.name
        fldict['Date'] = date
        fldict['Error'] = flagerror
        fldict['Slack'] = slack
        
        def debugging(fldict):
            print(fldict)
        debugging(fldict)

        def db_data():
            return 1

main()



