
def henkan(a):
    tyou = 0
    oku = 0
    man = 0
    if "*" in a :
        count = len(a)
        a = a[count+1:]

    if "兆" in a :
        count = a.index("兆")
        tyou = int(a[0:count])
        a = a[count+1:]
    if "億" in a :
        count = a.index("億")
        oku = int(a[0:count])
        a = a[count+1:]
    if "万" in a :
        count = a.index("万")
        man = int(a[0:count])
        a = a[count+1:]
    s = tyou*10000 + oku + man/10000
    return s
