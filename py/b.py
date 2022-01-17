import re
from random import choice

понятие = """Понятие
Элемент
Обозначение""".split('\n')

включает = """включает в себя такие понятия как:
включает в себя такие понятия:
состоит из:
связан с понятиями:""".split('\n')

def enumerate_list(a_list):
    if len(a_list) > 2:
        b_list = a_list[:-1]
        c = a_list[-1]
        out = ", ".join(b_list) + " и " + c
    elif len(a_list) == 2:
        b = a_list[0]
        c = a_list[-1]
        out = b + " и " + c
    return out
x = open('/tmp/rules.in').readlines()

G = {}
for line in x:
    try:
        a, b = [ x.strip() for x in re.findall(r'(.*?)->(.*?)\[', line.replace('"',''))[0] ]
        try:
            G[a] += [b]
        except KeyError:
            G.update({a:[b]})
    except IndexError:
        pass

keys = ["иммунохроматографический анализ"] + list(set(G.keys()) - {"иммунохроматографический анализ"})

for key in keys:
    items = G[key]
    if len(items) == 1:
        print(choice(понятие), key, 'представляет собой', items[0], ".")
    else:
        print(choice(понятие), key, 'включает в себя такие понятия как', enumerate_list(items), ".")
        
