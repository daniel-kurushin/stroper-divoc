from utilites import load

db = load('db.json')

for x in sorted(db.keys()):
    t = db[x][0]
    x = x.capitalize()
    print(f"{x}: {t}")