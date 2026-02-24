from sly import Lexer

class SVGLexer(Lexer):
    tokens = { OPEN_TAG, CLOSE_TAG, SELF_CLOSING }

    # Ignorar espacios/tabs/CR (NO \n para poder contar líneas)
    ignore = ' \t\r'

    def __init__(self):
        super().__init__()
        self._tagname = None
        self._attrs = {}

    # Contar líneas 
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Etiqueta de cierre: </rect>
    @_(r'</[a-zA-Z_][a-zA-Z0-9_:\-]*\s*>')
    def CLOSE_TAG(self, t):
        name = t.value[2:-1].strip()   # quita </ y >
        t.value = (name, {})           # cierre => sin atributos
        return t

    # Inicio de etiqueta de apertura: <rect  (sin cerrar todavía)
    @_(r'<[a-zA-Z_][a-zA-Z0-9_:\-]*')
    def OPEN_TAG(self, t):
        self._tagname = t.value[1:]    # quita '<'
        self._attrs = {}              # reinicia attrs de ESTA etiqueta
        self.begin(AttributeLexer)    # pasamos a leer atributos y el cierre > o />
        return None                   # todavía no devolvemos token


class AttributeLexer(Lexer):
    # Incluimos ATTRIBUTE para que la regla sea válida; lo descartamos devolviendo None
    tokens = { OPEN_TAG, SELF_CLOSING, ATTRIBUTE }

    ignore = ' \t\r'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # atributo="valor" 
    @_(r'[a-zA-Z_][a-zA-Z0-9_:\-]*="[^"]*"')
    def ATTRIBUTE(self, t):
        name, value = t.value.split('=', 1)
        self._attrs[name] = value[1:-1]   # quita las comillas
        return None                       # no emitimos token por atributo

    # Cierre normal de apertura: >
    @_(r'>')
    def OPEN_TAG(self, t):
        t.value = (self._tagname, dict(self._attrs))
        self.begin(SVGLexer)
        return t

    # Autocierre: />
    @_(r'/>')
    def SELF_CLOSING(self, t):
        t.value = (self._tagname, dict(self._attrs))
        self.begin(SVGLexer)
        return t

    def error(self, t):
        # Para no quedarte en bucle si aparece algo raro dentro de la etiqueta
        print(f"Caracter ilegal en atributos: {t.value[0]!r} (linea {self.lineno})")
        self.index += 1


# Primer test
for token in SVGLexer().tokenize('<rect x="10" y="10" width="100" height="100"/>'):
    print(token)

test = """
<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="20" width="100" height="50" fill="red" />
  <rect x="30" y="80" width="120" height="60" fill="blue" />
  <rect x="160" y="40" width="80" height="100" fill="green" />
  <circle cx="80" cy="150" r="25" fill="orange" />
  <ellipse cx="200" cy="150" rx="40" ry="20" fill="purple" />
</svg>
"""

for token in SVGLexer().tokenize(test):
    print(token)
