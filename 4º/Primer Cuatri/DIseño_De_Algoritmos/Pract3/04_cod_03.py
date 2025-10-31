# -*- coding: utf-8 -*-

# 04_cod_03.py
#
# Clase para las soluciones parciales del problema «set
# cover».

def carga_datos(fich):
    """Lee del fichero «fich» los datos de entrada. A modo de
    ejemplo, el fichero
    ----------
    0: 1 2 3
    1: 1 2 4
    2: 2 5
    ----------
    representa los tres conjuntos siguientes:
    {1, 2, 3}, {1, 2, 4} y {2, 5}. Los elementos de los
    conjuntos deben ser números enteros.

    Devuelve una lista, cada una de cuyas entradas está
    compuesta por la etiqueta de un conjunto y el propio
    conjunto, y el cardinal de la unión de todos esos
    conjuntos.
    """

    f = open(fich)
    fichas = list()
    etiquetas = list()
    subyacente = set()
    for l in f:
        l = l.split()
        etiq = l[0][:-1]
        if etiq in etiquetas:
            raise BaseException('Etiquetas repetidas')
        etiquetas.append(etiq)
        aux = set([int(x) for x in l[1:]])
        fichas.append([etiq, aux])
        subyacente.update(aux)
    f.close()
    return fichas, len(subyacente)

class Parcial:
    """Un objeto miembro es una colección de conjuntos."""

    def __init__(self, fich=None):
        """Genera un objeto vacío."""

        # Conjuntos y cardinal de su unión
        self.fichas, self.cardinal\
            = carga_datos(fich) if fich else (list(), 0)

        self.miembros = list()
        self.habilidades = set()

    def __repr__(self):
        return '{' + ', '.join\
            ([self.fichas[i][0] for i in self.miembros]) + '}'

    def copia(self):
        aux = self.__class__()
        aux.fichas = [[etiq, habs.copy()]\
                      for etiq, habs in self.fichas]
        aux.cardinal = self.cardinal
        aux.miembros = self.miembros.copy()
        aux.habilidades = self.habilidades.copy()
        return aux

    def libre(self):
        """Índice siguiente al último miebro."""

        if self.miembros:
            return self.miembros[-1] + 1
        else:
            return 0

    def amplía(self):
        """Generador de las ampliaciones con un conjunto
        situado después del último de self.
        """

        lib = self.libre()
        i = lib
        for etiq, habs in self.fichas[lib:]:
            ap = self.copia()
            ap.miembros.append(i)
            ap.habilidades.update(habs)
            yield ap
            i += 1

    def es_completa(self):
        return len(self.habilidades) == self.cardinal

    def coste(self):
        return len(self.miembros)

    def restos(self):
        """Habilidades aportadas por los candidatos que
        podrían acceder al grupo.
        """

        lib = self.libre()
        for etiq, habs in self.fichas[lib:]:
            yield habs.difference(self.habilidades)
