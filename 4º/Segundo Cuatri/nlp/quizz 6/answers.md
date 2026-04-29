# Quiz 6

## Pregunta 1: CNF

Gramatica original:

```text
A -> B C
B -> A
B -> B D E
```

Paso 1: eliminar la produccion unitaria `B -> A`.

Como `A -> B C`, sustituimos `B -> A` por:

```text
B -> B C
```

Paso 2: binarizar la regla de longitud 3:

```text
B -> B D E
```

La forma CNF equivalente es:

```text
A -> B C
B -> B C
B -> B X
X -> D E
```

En la captura, la opcion correcta es la que tiene esa estructura. La opcion esperada es la tercera:

```text
A -> B C
B -> B C
B -> B @D_E
@D_E -> D E
```

Nota: si el test considerase que el nombre del no terminal auxiliar es arbitrario, la opcion 2 tendria la misma forma estructural. Pero la transformacion correcta es exactamente la anterior.

## Pregunta 2: siguiente celda CKY

Celda izquierda:

```text
NNS = 0.0023
VB  = 0.001
```

Celda derecha:

```text
PP  = 0.2
IN  = 0.0014
NNS = 0.0001
```

Reglas relevantes:

```text
NP -> NNS NNS : 0.01
NP -> NNS PP  : 0.01
VP -> VB PP   : 0.045
VP -> VB NP   : 0.015
```

Calculamos las combinaciones binarias posibles para la siguiente celda:

1. `NP -> NNS NNS`

```text
0.01 * 0.0023 * 0.0001 = 2.3e-9
```

2. `NP -> NNS PP`

```text
0.01 * 0.0023 * 0.2 = 4.6e-6
```

3. `VP -> VB PP`

```text
0.045 * 0.001 * 0.2 = 9e-6
```

No podemos usar `VP -> VB NP` todavia porque en la celda derecha no hay `NP`.

La regla `PP -> IN : 0.002` no corresponde a esta siguiente celda combinada; esa es una produccion unaria sobre una sola celda. El valor trampa seria:

```text
0.002 * 0.0014 = 2.8e-6
```

pero no es la respuesta pedida aqui.

### Respuesta final de la Pregunta 2

La siguiente celda contiene:

```text
NP = max(2.3e-9, 4.6e-6) = 4.6e-6
VP = 9e-6
```

Por tanto, en el test hay que marcar:

- `NP: 4.6*10^-6`
- `VP: 9*10^-6`

No hay que marcar:

- `PP: 2.8*10^-6`
- `NP: 2.3*10^-9`
