def guardaBD(bd):
    file = open("PL2022pubs.txt", "w", encoding="utf-8")
    for line in bd:
        w = line["chaveCit"] + ";" + line["titulo"] + ";"
        for aut in line["autores"]:
            w = w + aut[0] + "," + aut[1] + "#"
        w = w[:-1] + ";"
        w = w + line["ano"] + ";" + line["local"] + "\n"
        file.write(w)

def lerBD(filename):
    file = open(filename, "r", encoding="utf-8")
    bd = []
    for line in file:
        reg = {}
        elems = line.split(";")
        reg["chaveCit"] = elems[0]
        reg["titulo"] = elems[1]
        reg["autores"] = []
        auts = elems[2].split("#")
        for aut in auts:
            names = aut.split(",")
            reg["autores"].append((names[0], names[1]))
        reg["ano"] = int(elems[3])
        reg["local"] = elems[4]
        bd.append(reg)
    return bd