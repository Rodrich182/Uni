infinito = float('inf')

def lanza(p, mj=None, t_mj=infinito):
    ct = p.cota()
    fondo = p.es_completa()
    escribe_línea(p, ct, t_mj, fondo, mejora)
    if ct < t_mj:
        if fondo:
            mj = p
            t_mj = ct
        else:
            for ap in p.amplía():
                mj, t_mj = lanza(ap, mj, t_mj)
    return mj, t_mj

p0 = Parcial_ct('04_dat_01.txt')
resp = lanza(p0)
print(resp, resp.coste)
