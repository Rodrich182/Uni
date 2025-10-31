#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# 04_cod_08.py
#
# Algoritmo de tipo «branch & bound» aplicado al problema
# «set cover».

import importlib
pcl = importlib.import_module('04_cod_11')

infinito = float('inf')

def bb(fich):
    return lanza(pcl.Parcial_ct(fich))

def lanza(p, mj=None, t_mj=infinito):
    fondo = p.es_completa()
    if fondo or t_mj < infinito:
        ct = p.cota()
        mejora = ct < t_mj
    else:
        # Es innecesario calcular la cota.
        ct = '—'
        mejora = True
    escribe_línea(p, ct, t_mj, fondo, mejora)
    if mejora:
        if fondo:
            mj = p
            t_mj = ct
        else:
            for ap in p.amplía():
                mj, t_mj = lanza(ap, mj, t_mj)
    return mj, t_mj

def escribe_número(x):
    return '∞' if x == infinito else str(x)

def escribe_línea(p, ct, t_mj, completa=False, mejora=False):
    récord = '[' + escribe_número(t_mj) + ']'
    código = '↓' if completa else ' '
    código += '✗' if not mejora else '✓'\
              if completa else '…'
    print('{0:>6s} {1:>6s}'.\
          format(récord, escribe_número(ct)),
          código, p)

if __name__ == '__main__':
    import sys
    fich = sys.argv[1] if len(sys.argv) > 1\
           else '04_dat_01.txt'
    print(bb(fich))
