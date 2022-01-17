import re
from utilites import load

text = open('../report 2021.md').read()
db = load('db.json')

n = 1
lit_dict = {}
for t in db.keys():
    if db[t][0] != "":
        text = text.replace(t, f"{t} [a{n}]", 3)
        lit_dict.update({f"[a{n}]": db[t][1]})
        n += 1
    
lit = []
n = 1
for a in re.findall(r'\[a\d+\]', text):
    text = text.replace(a, f'[{n}]')
    link = re.findall(r'\[(.*?)\]', lit_dict[a])[0]
    if link not in lit:
        lit += [link]
    n += 1
    
n = 1
for l in lit:
    print(n, l)
    n += 1
    
open('../report 2021.md.1','w').write(text)