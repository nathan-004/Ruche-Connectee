# Imports go at the top
from microbit import *
import log

def str_list(liste, sep=""):
    res = ""

    for el in liste:
        res += sep + str(el)

    return res[1:]

def copy(liste):
    t = []

    for el in liste:
        t.append(el)

    return t

FIRST_DATE = [0,29,23,59,59]
date = copy(FIRST_DATE) # m, j, h, m, s

saisons = ("hiver",
    "hiver",
    "hiver",
    "printemps",
    "printemps",
    "printemps",
    "ete",
    "ete",
    "ete",
    "automne",
    "automne",
    "automne"
)

saison = saisons[FIRST_DATE[0] - 1]

@run_every(s=1)
def modify_date():

    t = [12, 30, 24, 60, 60]
    date[-1] += 1
    
    for i in range(len(t)-1, -1, -1):
        if date[i] >= t[i]:
            if i != 0:
                date[i-1] += 1
                date[i] %= t[i]
            else:
                date[i] %= t[i]
    
    if date[0] != FIRST_DATE[0]:
        saison = saisons[date[0] - 1]

@run_every(min=15)
def send_data():
    pass
    
while True:
    d = {"date": str_list(date, "-"), "saison": saison}
    print(d)
    sleep(1000)
