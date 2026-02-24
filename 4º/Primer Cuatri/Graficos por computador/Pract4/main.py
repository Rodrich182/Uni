
import tkinter as tk

import dictionary as D
from LineDrawing import ALGO_REGISTRY
from gui import LineDrawingGUI

def draw_line(start, end, algo_name=None):
    """
    start/end: tuplas (x, y) en coordenadas lógicas
    algo_name: clave opcional; si no se pasa se usa el global activo
    """
    x1, y1 = start
    x2, y2 = end

    key = algo_name or D.SETTINGS.get("active_line_algorithm", D.DEFAULT_LINE_ALGO)
    func = ALGO_REGISTRY.get(key)
    if not func:
        return []
    return func(x1, y1, x2, y2)

if __name__ == "__main__":
    """This starts the GUI application."""
    root = tk.Tk()
    app = LineDrawingGUI(
        root,
        draw_callback=draw_line,
        algo_keys=D.LINE_ALGORITHM_KEYS,
        default_algo=D.SETTINGS["active_line_algorithm"],
        canvas_size=D.CANVAS_SIZE,
        default_pixel_size=D.DEFAULT_PIXEL_SIZE,
        title=D.APP_TITLE,
        win_size=D.WINDOW_SIZE,
    )
    root.mainloop()