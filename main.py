from pathlib import Path
import re
import os

#flnamedict = dict()
#flslackdict = dict()
#fldatedict = dict()
#flerrordict = dict()

#fldict = dict()

listlog = os.listdir('log')
#print(listlog)

#flagerror = False
#logpath = 'log/prebuf_resynth.log'
#log = open(logpath)
#path = Path(logpath)
#date = ''
#slack = []

for logpath in listlog:

    if Path(logpath).suffix != '.log':
        continue

    fldict = dict()

    flagerror = False
    logpath = 'log/' + logpath
    log = open(logpath)
    path = Path(logpath)
    date = ''
    slack = []
    flagdate = False

    #для отладки
    print(path.name)

    while True:

        line = log.readline().strip()

        if not line:
            fldict['Filename'] = path.name
            fldict['Error'] = flagerror
            fldict['Date'] = date
            break
        
        #часть проверки времени, случай если время указано строчкой ниже
        if flagdate:
            date = line
            flagdate = False

        #поиск ошибки
        if ('ERROR' in line) or ('FATAL' in line):
            flagerror = True

        #поиск slack
        if (re.search(r'[Ss]lack', line)):
            continue
    
        #ищет время и выдает срез строки после найденных слов и когда появляется первая буква\цифра. span - кортеж из начала и конца найденного соответствия(индексы)
        if (re.search(r'([dD]ate)|([Ss]tart [tT]ime)', line)):
            span = re.search(r'([dD]ate)|([Ss]tart [tT]ime)', line).span()
            line = line[span[1]:]
            span = re.search(r'\w', line)
            if span:
                span = span.span()
                line = line[span[0]:]
                date = line
            else:
                flagdate = True

    print(fldict)


