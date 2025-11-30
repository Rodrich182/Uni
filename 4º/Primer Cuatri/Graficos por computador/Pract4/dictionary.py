
APP_TITLE = "Visualizador de Algoritmos de Línea"
WINDOW_SIZE = "900x650"
CANVAS_SIZE = 600

DEFAULT_PIXEL_SIZE = 8

LINE_ALGORITHM_KEYS = [
    "slope_intercept_modified",
    "dda_algorithm",
    "bresenham_integer",
    "slope_intercept_basic",
]

DEFAULT_LINE_ALGO = "bresenham_integer"
DEFAULT_THEME = "light" #puedo poner "dark"

# Nuevo: prácticas
PRACTICE_KEYS = ["practica1", "practica2", "practica3", "practica4"]
DEFAULT_PRACTICE = "practica1"

SETTINGS = {
    "active_line_algorithm": DEFAULT_LINE_ALGO,
    "pixel_size": DEFAULT_PIXEL_SIZE,
    "theme": DEFAULT_THEME,
    "practice": DEFAULT_PRACTICE,
}


FRACTAL_RECURSIVE_TYPES = ("sierpinski", "koch")
DEFAULT_FRACTAL_RECURSIVE = "sierpinski"

FRACTAL_IFS_TYPES = ("barnsley", "sierpinski_ifs")
DEFAULT_FRACTAL_IFS = "barnsley"

DEFAULT_FRACTAL_LEVEL = 4        # nivel de recursión por defecto
DEFAULT_FRACTAL_ITER = 80        # iteraciones por defecto para Mandelbrot / Julia
DEFAULT_IFS_ITER = 50000         # iteraciones probabilistas para IFS
DEFAULT_IFS_SKIP = 100           # iteraciones iniciales a descartar (semilla)

# --- Parámetros por defecto L-systems (Práctica 4) ---

L_SYSTEM_KEYS = ["koch", "sierpinski", "dragon", "planta"]
DEFAULT_L_SYSTEM = "planta"

DEFAULT_LSYS_ITER = 3        # iteraciones iniciales
MAX_LSYS_ITER = 7            # tope razonable para no explotar la cadena

DEFAULT_LSYS_ANGLE = 25.0    # grados por defecto (se sobreescribe por preset)
DEFAULT_LSYS_LENGTH = 5.0    # longitud de segmento por defecto
