# -*- coding: utf-8 -*-

# 04_cod_06.py
#
# Clase para las soluciones parciales del problema «set
# cover», incluyendo una cota para su abordaje mediante el
# método de «branch and bound».

import importlib
base = importlib.import_module('04_cod_03')

class Parcial_ct(base.Parcial):

    def cota(self):
        aux = self.coste()
        # if self.es_completa():
        #     return aux
        hab_faltan = self.cardinal - len(self.habilidades)
        rt = sorted([len(ct) for ct in self.restos()],
                    reverse=True)
        for r in rt:
            if hab_faltan <= 0:
                break
            hab_faltan -= r
            aux += 1
        return float('inf') if hab_faltan > 0 else aux
