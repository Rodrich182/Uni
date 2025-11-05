#lang racket
;;6) Compara, utilizando datos de entrada generados aleatoriamente, los resultados del algoritmo de tipo
;; branch and bound con los del algoritmo voraz que has completado en (2).
;;
;;Uso estos Comandos:
;;python 04_cod_10.py 16 80 10
;;Me tarda poco y tanto Voraz como BnB me dan lo mismo en la mayoria de casos, a que andamos en un caso relativamente sencillo
;;
|#
PS C:\Users\rodrich\Documents\AA uni\Repositorio\4o\Primer Cuatri\DIseño_De_Algoritmos\Pract3> python 04_cod_10.py 16 80 10 
Voraz: 13 miembros
B & B: 13 miembros
PS C:\Users\rodrich\Documents\AA uni\Repositorio\4o\Primer Cuatri\DIseño_De_Algoritmos\Pract3> python 04_cod_10.py 16 80 10
Voraz: 14 miembros
B & B: 14 miembros
PS C:\Users\rodrich\Documents\AA uni\Repositorio\4o\Primer Cuatri\DIseño_De_Algoritmos\Pract3> python 04_cod_10.py 16 80 10
Voraz: 11 miembros
B & B: 10 miembros <-
PS C:\Users\rodrich\Documents\AA uni\Repositorio\4o\Primer Cuatri\DIseño_De_Algoritmos\Pract3> python 04_cod_10.py 16 80 10
Voraz: 12 miembros
B & B: 12 miembros

#|
;;python 04_cod_10.py 24 120 12 
;;Sigue sucediendo como en el caso anterior, aunque si que es mas apreciable la diferencia entre voraz y BnB
;;
|#
PS C:\Users\rodrich\Documents\AA uni\Repositorio\4o\Primer Cuatri\DIseño_De_Algoritmos\Pract3> python 04_cod_10.py 24 120 12
Voraz: 16 miembros
B & B: 15 miembros<-
PS C:\Users\rodrich\Documents\AA uni\Repositorio\4o\Primer Cuatri\DIseño_De_Algoritmos\Pract3> python 04_cod_10.py 24 120 12
Voraz: 24 miembros
B & B: 24 miembros
PS C:\Users\rodrich\Documents\AA uni\Repositorio\4o\Primer Cuatri\DIseño_De_Algoritmos\Pract3> python 04_cod_10.py 24 120 12
Voraz: 22 miembros
B & B: 20 miembros<_-
PS C:\Users\rodrich\Documents\AA uni\Repositorio\4o\Primer Cuatri\DIseño_De_Algoritmos\Pract3> python 04_cod_10.py 24 120 12
Voraz: 17 miembros
B & B: 17 miembros
#|
;;
;;python 04_cod_10.py 32 137 12
;;Aqui ya aumenta el numero de casos con diferencias y las propias diferencias se hacen mas grandes.
|#
PS C:\Users\rodrich\Documents\AA uni\Repositorio\4o\Primer Cuatri\DIseño_De_Algoritmos\Pract3> python 04_cod_10.py 32 137 12 
Voraz: 25 miembros
B & B: 24 miembros<-
PS C:\Users\rodrich\Documents\AA uni\Repositorio\4o\Primer Cuatri\DIseño_De_Algoritmos\Pract3> python 04_cod_10.py 32 137 12
Voraz: 27 miembros
B & B: 26 miembros<-
PS C:\Users\rodrich\Documents\AA uni\Repositorio\4o\Primer Cuatri\DIseño_De_Algoritmos\Pract3> python 04_cod_10.py 32 137 12
Voraz: 23 miembros
B & B: 22 miembros<-
PS C:\Users\rodrich\Documents\AA uni\Repositorio\4o\Primer Cuatri\DIseño_De_Algoritmos\Pract3> python 04_cod_10.py 32 137 12
Voraz: 29 miembros
B & B: 29 miembros
#|