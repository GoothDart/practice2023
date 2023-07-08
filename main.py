from pathlib import Path

#flnamedict = dict()
#flslackdict = dict()
#fldatedict = dict()
#flerrordict = dict()

fldict = dict()

flagerror = False
logpath = 'log/prebuf_resynth.log'
log = open(logpath)
path = Path(logpath)


while True:

    line = log.readline().strip()

    if not line:
        fldict['Filename'] = path.name
        fldict['Error'] = flagerror
        break

    if ('ERROR' in line) or ('FATAL' in line):
        flagerror = True


print(fldict)


