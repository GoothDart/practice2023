from pathlib import Path
import re

#flnamedict = dict()
#flslackdict = dict()
#fldatedict = dict()
#flerrordict = dict()

fldict = dict()

flagerror = False
logpath = 'log/prebuf_resynth.log'
log = open(logpath)
path = Path(logpath)
date = ''
slack = []

while True:

    line = log.readline().strip()

    if not line:
        fldict['Filename'] = path.name
        fldict['Error'] = flagerror
        fldict['Date'] = date
        break

    if ('ERROR' in line) or ('FATAL' in line):
        flagerror = True

    if (re.search(r'[Ss]lack', line)):
        continue
    
    if (re.search(r'([dD]ate)|([Ss]tart [tT]ime)', line)):
        span = re.search(r'([dD]ate)|([Ss]tart [tT]ime)', line).span()
        line = line[span[1]:]
        span = re.search(r'\w', line).span()
        line = line[span[0]:]
        date = line

print(fldict)


