# Proyecto personal: MiniLang

MiniLang es un lenguaje imperativo pequeño con funciones, bloques y ámbitos léxicos.  
El proyecto está implementado en Python usando obligatoriamente `sly` para el análisis léxico y sintáctico, y cumple con los requisitos de la práctica: construcción de AST, gestión de ámbitos, chequeo semántico, ejecución mediante intérprete y varios tests automáticos.

## 1. Lenguaje fuente

MiniLang está pensado para enseñar de forma compacta las fases principales de un procesador de lenguajes:

- análisis léxico con `sly.Lexer`
- análisis sintáctico con `sly.Parser`
- construcción de árbol abstracto de sintaxis
- chequeo semántico con tabla de símbolos y ámbitos anidados
- interpretación directa del programa

### Características del lenguaje

- declaraciones de variables con `let`
- funciones con parámetros tipados y tipo de retorno
- bloques `{ ... }` con sombreado de nombres
- condicionales `if / else`
- bucles `while`
- `return`
- `print`
- tipos básicos `int`, `bool` y `void`
- operadores aritméticos, relacionales y lógicos

### Ejemplo

```txt
fun fact(n: int) -> int {
    if (n <= 1) {
        return 1;
    }
    return n * fact(n - 1);
}

print fact(6);
```

## 2. Sintaxis resumida

```txt
programa        ::= declaracion*
declaracion     ::= funcion | sentencia
funcion         ::= "fun" ID "(" parametros? ")" "->" tipo bloque
parametros      ::= parametro ("," parametro)*
parametro       ::= ID ":" tipo

sentencia       ::= "let" ID ":" tipo ("=" expresion)? ";"
                  | ID "=" expresion ";"
                  | "print" expresion ";"
                  | "if" "(" expresion ")" sentencia ("else" sentencia)?
                  | "while" "(" expresion ")" sentencia
                  | "return" expresion? ";"
                  | bloque
                  | expresion ";"

bloque          ::= "{" sentencia* "}"
tipo            ::= "int" | "bool" | "void"
```

## 3. Gestión de ámbitos

El proyecto implementa ámbitos léxicos reales:

- existe un ámbito global
- cada bloque crea un ámbito hijo
- cada función crea su propio ámbito para parámetros y variables locales
- una búsqueda de identificador recorre los ámbitos desde el interno al externo
- se permite sombreado entre ámbitos distintos
- se rechazan redefiniciones dentro del mismo ámbito

Esto permite demostrar variables locales, variables globales, sombreado y llamadas recursivas.

## 4. Estructura del proyecto

```txt
minilang/
    ast.py          AST + visitor
    lexer.py        analizador léxico con SLY
    parser.py       analizador sintáctico con SLY
    checker.py      chequeo semántico y tabla de símbolos
    interpreter.py  intérprete del lenguaje
    errors.py       jerarquía de errores
    __main__.py     CLI

examples/
    factorial.mini
    scopes.mini
    loop_and_void.mini

tests/
    test_minilang.py
```

## 5. Decisiones de diseño

- Se ha elegido un intérprete en lugar de un traductor porque permite enseñar de forma directa el AST, el chequeo semántico y la ejecución.
- El lenguaje es pequeño pero suficientemente rico para mostrar funciones, bloques y ámbitos.
- Se han usado tipos explícitos para reforzar la fase semántica.
- Las funciones se predeclaran en el ámbito global para permitir recursión.
- El análisis semántico comprueba, entre otras cosas:
  - uso de nombres no declarados
  - redeclaraciones en el mismo ámbito
  - compatibilidad de tipos
  - aridad de llamadas
  - uso correcto de `return`

## 6. Cómo ejecutarlo

### Ejecutar un programa

```bash
python -m minilang examples/factorial.mini
```

### Ver el AST

```bash
python -m minilang examples/factorial.mini --ast
```

### Ver los tokens

```bash
python -m minilang examples/factorial.mini --tokens
```

### Solo analizar sin ejecutar

```bash
python -m minilang examples/factorial.mini --check
```

## 7. Tests

La práctica incluye tests automáticos de integración para:

- recursión
- ámbitos y sombreado
- bucles
- lógica booleana
- funciones `void`
- errores semánticos
- error de ejecución por falta de `return`

Ejecutar:

```bash
python -m unittest discover -s tests
```

## 8. Ideas para la presentación oral

En 10 minutos puedes enseñar esta secuencia:

1. Explicar el lenguaje y por qué se eligió un subconjunto razonable.
2. Mostrar el lexer y el parser en `sly`.
3. Enseñar el AST y la tabla de símbolos.
4. Ejecutar `examples/scopes.mini` para justificar la gestión de ámbitos.
5. Ejecutar `examples/factorial.mini` para mostrar funciones y recursión.
6. Ejecutar los tests para demostrar que el proyecto es funcional.
