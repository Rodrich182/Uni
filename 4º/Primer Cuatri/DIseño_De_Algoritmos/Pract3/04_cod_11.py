# -*- coding: utf-8 -*-

# 04_cod_11.py
#
# Clase para las soluciones parciales del problema «set
# cover», incluyendo una cota para su abordaje mediante el
# método de «branch and bound».

import math
import importlib
base = importlib.import_module('04_cod_03')

class Parcial_ct(base.Parcial):

    def cota(self):
        hay = self.coste()
        if self.es_completa():
            return hay
        hab_faltan = self.cardinal - len(self.habilidades)
        todas = set()
        mayor_incr = 0
        for r in self.restos():
            todas.update(r)
            if len(r) > mayor_incr:
                mayor_incr = len(r)
        if len(todas) < hab_faltan or mayor_incr == 0:
            return math.inf
        else:
            return hay + math.ceil(hab_faltan / mayor_incr)
