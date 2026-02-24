# -*- coding: cp1252 -*-

import sys
import re

reg="^((\d{1,3})\s([0-1A-Z])\s(\d{1,3})\s([0-1A-Z])\s[LR])\s*(?:#.*)?$"

class Maquina(object):
    """
    Clase que representa una maquina Turing
    """

    def __init__(self, Q = {"q0"}, q0 = "q0", Gamma = {}, delta = {}):
        """
        Constructor que simplemente inicializa el conjunto de estados,
        el alfabeto de la cinta y la funcion de transicion.
        """
        self.Q = Q
        self.q0 = q0
        self.Gamma = Gamma if Gamma else set()
        self.delta = delta if delta else dict()
        self.posicion = 0
        self.q = self.q0



    def movimiento(self, cinta):
        """
        Este metodo simula una iteracion de la maquina Turing
        Argumentos:
        - cinta: La cinta es un string que representa el contenido
        de la cinta
        Devuelve una tupla (cinta_ext, salida) donde:
        - cinta_ext es el contenido de la cinta despues de un movimiento
        - salida es o una lista vacia, si no hay mas movimientos
        posibles, o la lista [p,Y,D] si self.delta[(self.q,X)]=(p,Y,D)
        (si X es la letra actualmente senalada por el cabezal) 
        """
        cinta_ext = cinta
        letra = cinta_ext[self.posicion]
        salida = self.delta.get ((self.q, letra), [])
        if not salida:
            return cinta_ext, []
        cinta_ext = cinta_ext[:self.posicion] + salida[1]+ cinta_ext[self.posicion+1:]
        self.q = salida[0]
        if salida[2] == 'L':
            if self.posicion:
                self.posicion -= 1
            else:
                cinta_ext="B"+cinta_ext 
        else:
            if len(cinta)-self.posicion==1:
                cinta_ext=cinta_ext+"B"
            self.posicion += 1            
        return cinta_ext, salida

    def computacion(self, palabra):
        """
        Este metodo simula la computacion de una 
        maquina Turing para una cierta entrada
        """
        self.q = self.q0
        self.posicion = 0
        cinta, salida = self.movimiento(palabra)
        while salida:
            cinta, salida = self.movimiento(cinta)
        return cinta.strip("B")


    def lee_fichero(self, nombre_de_archivo):
        """
        Este metodo lee la maquina Turing de un fichero de texto en
        claro y sobreescribe los atributos de la clase
        Argumentos:
        - nombre_de_archivo: El nombre del archivo de texto donde
        esta la maquina
        """
        datos=[]
        states,symbols=set(),set()
        for line in open(nombre_de_archivo, 'r'):
            m=re.search(reg,line)
            if m:
                datos.append(m.group(1))
                states.add(int(m.group(2)))
                states.add(int(m.group(4)))
                symbols.add(m.group(3))
                symbols.add(m.group(5))
            elif line[0]!="#":
                print("Verifica esta linea",line.strip())
                return False
        states=sorted(states)
        symbols=sorted(symbols)
        if 0 not in states:
            print("Esta maquina no hace nada, vuelve a modificar el fichero")
            return False
        if len(datos)==0:
            print("Esta maquina no hace nada, vuelve a modificar el fichero")
            return False
        self.Q = ['q'+str(i) for i in states]      
        self.Gamma = symbols
        for trans in datos:
            l= trans.split()
            self.delta[('q'+l[0],l[1])]=('q'+l[2],l[3],l[4])
        return True


def nicelyprint(mystring):
    toprint=""
    m=re.search("^(1+)(?:0(1+))?$",mystring)
    if m:
        toprint=str(len(m.group(1))-1)
        if m.group(2):
            toprint+=" "+str(len(m.group(2))-1)
    return toprint




if __name__ == '__main__':
    filenameTM="ejemplo.tm"
    rango1,rango2=5,5
    if len(sys.argv)>=2:
        filenameTM=sys.argv[1]
        narg=len(sys.argv)
        rango1=int(sys.argv[2]) if narg>=3 else 1
        rango2=int(sys.argv[3]) if narg>=4 else 0
    if rango2:
        listofinputs=["".join(["1"]*(i+1)+["0"]+["1"]*(j+1)) for i in range(rango1) for j in range(rango2)]
    else:
        listofinputs=["".join(["1"]*(i+1)) for i in range(rango1)]
    t=Maquina() 
    if t.lee_fichero(filenameTM):
        for inp in listofinputs:
            print("Configuracion inicial: %s corresponde a: %s"%(inp,nicelyprint(inp)))
            out=t.computacion(inp)
            if nicelyprint(out):
                print("Salida: %s corresponde a: %s"%(out,nicelyprint(out)))
            else:
                print("Salida: %s"%out)


