# archivo: main.py

from gui import LineDrawingGUI
from slope_intercept_basic import slope_intercept_basic
from slope_intercept_modified import slope_intercept_modified
from dda_algorithm import dda_algorithm
from bresenham_real import bresenham_real
from bresenham_integer import bresenham_integer
import tkinter as tk

def draw_line(start, end, algo_name):
    x1, y1 = start
    x2, y2 = end
    if algo_name == "slope_intercept_basic":
        return slope_intercept_basic(x1, y1, x2, y2)
    if algo_name == "slope_intercept_modified":
        return slope_intercept_modified(x1, y1, x2, y2)
    if algo_name == "dda_algorithm":
        return dda_algorithm(x1, y1, x2, y2)
    if algo_name == "bresenham_real":
        return bresenham_real(x1, y1, x2, y2)
    if algo_name == "bresenham_integer":
        return bresenham_integer(x1, y1, x2, y2)
    return []

if __name__ == "__main__":
    root = tk.Tk()
    app = LineDrawingGUI(root, draw_callback=draw_line)
    root.mainloop()
