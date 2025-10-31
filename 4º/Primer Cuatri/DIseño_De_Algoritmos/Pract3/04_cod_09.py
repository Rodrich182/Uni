#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# 04_cod_09.py
#
# Generador de unos datos de entrada aleatorios para el
# problema «set cover».

import random

def tirada(c, h, fich, t=None):
    """
    c: n.º de candidatos
    h: n.º de habilidades
    t: tope para las aptitudes de un candidato
    """

    f = open(fich, 'w')
    if not t:
        t = min(h, 12)
    tam1 = len(str(c))
    tam2 = len(str(h))
    for i in range(c):
        num = random.randint(1, t)
        habs = random.sample(range(h), num)
        f.write('{0:{1}d}:'.format(i, tam1))
        for x in habs:
            f.write(' {0:{1}d}'.format(x, tam2))
        f.write('\n')
    f.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print('04_cod_09.py <candidatos> <habilidades> '
              '<fichero de salida> [tope por persona]')
    else:
        c = int(sys.argv[1])
        h = int(sys.argv[2])
        tirada(c, h, sys.argv[3],
               int(sys.argv[4]) if len(sys.argv) > 4\
               else None)
