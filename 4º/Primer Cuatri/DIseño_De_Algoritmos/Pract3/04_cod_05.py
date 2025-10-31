# -*- coding: utf-8 -*-

# 04_cod_05.py
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
        rt = [len(ct) for ct in self.restos()]
        if rt:
            mayor = sorted(rt)[-1]
            if mayor == 0:
                return math.inf
            return hay + math.ceil(hab_faltan / mayor)
        else:
            return math.inf
