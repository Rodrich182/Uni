# -*- coding: utf-8 -*-

# 04_cod_04.py
#
# Clase para las soluciones parciales del problema «set
# cover», incluyendo una cota ingenua para su abordaje
# mediante el método de «branch and bound».

import importlib
base = importlib.import_module('04_cod_03')

class Parcial_ct(base.Parcial):

    def cota(self):
        return self.coste()
