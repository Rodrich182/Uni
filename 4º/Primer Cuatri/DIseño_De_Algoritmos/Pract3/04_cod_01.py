#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# 04_cod_01.py
#
# Estudio de los datos de entrada de un problema de tipo
# «set cover».

def carga_habs(fich):
    """Lee del fichero «fich» los datos de entrada. A modo de
    ejemplo, el fichero
    ----------
    0: 1 2 3
    1: 1 2 4
    2: 2 5
    ----------
    representa los tres conjuntos siguientes:
    {1, 2, 3}, {1, 2, 4} y {2, 5}. Los elementos de los
    conjuntos deben ser números enteros.

    Devuelve el conjunto de las habilidades que aparecen.
    """

    f = open(fich)
    # etiquetas = list()
    subyacente = set()
    for l in f:
        l = l.split()
        # etiq = l[0][:-1]
        # if etiq in etiquetas:
        #     raise BaseException('Etiquetas repetidas')
        # etiquetas.append(etiq)
        aux = set([int(x) for x in l[1:]])
        subyacente.update(aux)
    f.close()
    return subyacente

def es_rango(cjto, n):
    """Determina si un conjunto es el de los primeros n
    enteros (incluyendo 0).
    """

    return cjto == set(range(n))

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('04_cod_01.py <fichero> <n>')
    else:
        fich = sys.argv[1]
        n = int(sys.argv[2])
        cjto = carga_habs(fich)
        print('Salen %d habilidades.' % len(cjto))
        print(es_rango(cjto, n))
