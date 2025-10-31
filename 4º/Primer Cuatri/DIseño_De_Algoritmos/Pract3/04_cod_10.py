#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# 04_cod_10.py
#
# Genera un caso aleatorio para el problema «set cover» y
# comprueba las soluciones del algoritmo voraz y el de tipo
# «branch and bound».

import contextlib
import importlib
ej = importlib.import_module('04_cod_09')
vrz = importlib.import_module('04_cod_02')
bb = importlib.import_module('04_cod_08')

def compara(fich):
    p1 = vrz.voraz(fich)
    t1 = p1.coste()
    # Desechamos la información intermedia.
    with contextlib.redirect_stdout(open('/dev/null', 'w')):
        p2, t2 = bb.bb(fich)
    return t1, t2

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('04_cod_10.py <candidatos> <habilidades> '
              '[tope por persona]')
    else:
        import os
        import tempfile
        c = int(sys.argv[1])
        h = int(sys.argv[2])
        fich = tempfile.NamedTemporaryFile(suffix='.txt',
                                   delete=False).name
        ej.tirada(c, h, fich,
               int(sys.argv[3]) if len(sys.argv) > 3 else None)
        t1, t2 = compara(fich)
        print('Voraz: %d miembros' % t1)
        print('B & B: %g miembros' % t2)
        os.unlink(fich)
