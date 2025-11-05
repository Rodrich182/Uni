
from typing import List, Set, Tuple
import math
import importlib
base = importlib.import_module('04_cod_03')


class Parcial:
    def __init__(self, fich: str = None, H: List[Set[int]] = None,
                 universo: Set[int] = None, seleccion: Tuple[int, ...] = (),
                 cubiertas: Set[int] = None, siguiente: int = 0):
        if H is None:
            # Construcción raíz: cargar fichero
            self.H = []
            with open(fich, 'r', encoding='utf-8') as f:
                for line in f:
                    toks = line.strip().split()
                    if not toks:
                        continue
                    # toks[0] es el id; el resto son habilidades
                    habilidades = set(map(int, toks[1:]))
                    self.H.append(habilidades)
            self.universo = set().union(*self.H) if self.H else set()
            self.seleccion = tuple()
            self.cubiertas = set()
            self.siguiente = 0
        else:
            # Construcción interna: reutilizar estructuras
            self.H = H
            self.universo = universo
            self.seleccion = seleccion
            self.cubiertas = cubiertas if cubiertas is not None else set()
            self.siguiente = siguiente

    def __repr__(self):
        return f"Sel={list(self.seleccion)} | cubiertas={len(self.cubiertas)}/{len(self.universo)}"

    def coste(self) -> int:
        return len(self.seleccion)

    def es_completa(self) -> bool:
        return self.cubiertas.issuperset(self.universo)

    # Genera hijos añadiendo un candidato no usado aún (combinaciones, no permutaciones)
    def amplía(self):
        H, universo = self.H, self.universo
        for i in range(self.siguiente, len(H)):
            nueva_sel = self.seleccion + (i,)
            nuevas_cub = self.cubiertas | H[i]
            yield self.__class__(None, H, universo, nueva_sel, nuevas_cub, i + 1)

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
