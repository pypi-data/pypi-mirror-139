import datetime
def stamp():
    dt = str(datetime.datetime.now())
    s = dt.split(' ')
    d = s[0].split('-')
    r = d[::-1]
    t = s[1].split('.')[0]
    return f'[{"/".join(r)} {t}]'