# -*- coding: utf-8 -*-

# 04_cod_07.py
#
# Clase para las soluciones parciales del problema «set
# cover», incluyendo una estrategia voraz.

import importlib
base = importlib.import_module('04_cod_03')

class Parcial_vrz(base.Parcial):

    def mejor(self):
        aux = sorted(zip(self.fichas,
                         range(len(self.fichas))),
                     key=lambda t: len(t[0][1]))
        if aux and aux[-1][0][1]:
            return aux[-1][1]

    def amplía_voraz(self):
        i = self.mejor()
        if i != None:
            self.miembros.append(i)
            habs = self.fichas[i][1].copy()
            self.habilidades.update(habs)
            for n, ap in self.fichas:
                ap.difference_update(habs)

