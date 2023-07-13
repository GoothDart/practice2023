from pathlib import Path
import re
import os

namedir = input('введите имя папки')
listlog = os.listdir(namedir)

#поиск ошибки
def searcherror(line):
    if ('ERROR' in line) or ('FATAL' in line):
        span = re.search(r'(ERROR)|(FATAL)', line).span()
        if span[0] == 0:
            global flagerror
            flagerror = Trueflagerror = False

#поиск slack
#if re.search(r'([Rr]eport [Ss]lack)|(Initial slew slack)', line):
def searchworstslack(line):
    if re.search(r'[Ww]orst [Ss]lack', line):
        span = re.search(r'[Ww]orst [Ss]lack', line).span()
        line = line[span[1]:]
        line = line.split()
        for elem in line:
            if re.search(r'\d', elem):
                global slack
                slack.append(elem)

 #ищет время и выдает срез строки после найденных слов и когда появляется первая буква\цифра. span - кортеж из начала и конца найденного соответствия(индексы)
def searchdate(line):
    global flagdate
    global date
    if flagdate:
        date = line
        flagdate = False
    if re.search(r'(\b[dD]ate)|([Ss]tart [tT]ime)', line):
        span = re.search(r'(\b[dD]ate)|([Ss]tart [tT]ime)', line).span()
        line = line[span[1]:]
        span = re.search(r'\w', line)
        if span:
            span = span.span()
            line = line[span[0]:]
            date = line
        else:
            flagdate = True

for logpath in listlog:

    if Path(logpath).suffix != '.log':
        continue

    fldict = dict()
    
    flagerror = False
    logpath = namedir + '/' + logpath
    log = open(logpath)
    path = Path(logpath)
    date = ''
    slack = []
    flagdate = False

    for line in log:

        line = line.strip()
        
        #поиск ошибки
        searcherror(line)

        #ищет время и выдает срез строки после найденных слов и когда появляется первая буква\цифра. span - кортеж из начала и конца найденного соответствия(индексы)
        searchdate(line)

        #поиск slack
        searchworstslack(line)

    fldict['Filename'] = path.name
    fldict['Error'] = flagerror
    fldict['Date'] = date
    fldict['Slack'] = slack

    print(fldict)


