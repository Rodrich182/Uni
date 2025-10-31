#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# 04_cod_02.py
#
# Aproximación a la solución del problema «set cover»
# mediante una estrategia voraz.

import importlib
pcl = importlib.import_module('04_cod_07')

def voraz(fich):
    p = pcl.Parcial_vrz(fich)
    while not p.es_completa():
        p.amplía_voraz()
    return p

if __name__ == '__main__':
    import sys
    fich = sys.argv[1] if len(sys.argv) > 1\
           else '04_dat_01.txt'
    aux = voraz(fich)
    print(aux)
    print(aux.coste())
