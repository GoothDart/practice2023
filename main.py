#flnamedict = dict()
#flslackdict = dict()
#fldatedict = dict()
#flerrordict = dict()

fldict = dict()

flagerror = False
log = open('log/prebuf_resynth.log')

while True:
    line = log.readline().strip()
    if not line:
        break
        fldict['Error'] = flagerror
    if ('ERROR' in line) or ('FATAL' in line):
        flagerror = True


print(fldict)


