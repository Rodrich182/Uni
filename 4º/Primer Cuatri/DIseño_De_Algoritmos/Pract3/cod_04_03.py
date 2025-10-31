def voraz(fich):
    p = Parcial_vrz(fich)
    while not p.es_completa():
        p.amplía_voraz()
    return p

resp = voraz('04_dat_01.txt')
print(resp, resp.coste())
