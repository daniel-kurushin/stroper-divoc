from xlrd import open_workbook

_in = open_workbook('/tmp/in.xls').sheets()[0]

work = {}

for row in range(_in.nrows):
    k = _in.cell(row, 2).value
    item = _in.cell(row, 0).value
    price = str(_in.cell(row, 1).value)
    try:
        work[k] += [(item, price)]
    except KeyError:
        work.update({k:[(item, price)]})
        
def printitems(a, b, c=""):
    if len(b) > 1:
        d = 'приобретены'
    else:
        d = 'приобретен'
#    b = ", ".join(b)
    out = []
    for item, price in b:
        out += [item, "по цене", price, "руб."]
    print(" ".join([c, a, d, " ".join(out)]))

for k in work.keys():
    if "Для" in k:
        printitems(k, work[k])
    else:
        printitems(k.lower(), work[k], 'В качестве')
