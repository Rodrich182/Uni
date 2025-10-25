# archivo: gui.py

import tkinter as tk
from tkinter import ttk, messagebox

class LineDrawingGUI(ttk.Frame):
    def __init__(self, parent, draw_callback):
        """
        parent: ventana raíz de Tk
        draw_callback: función que recibe los dos puntos y el nombre de algoritmo
        """
        super().__init__(parent)
        self.parent = parent
        self.draw_callback = draw_callback
        self.parent.title("Visualizador de Algoritmos de Línea")
        self.parent.geometry("900x700")
        self.start = None
        self.end = None

        # Selección de algoritmo
        algos = [
            "slope_intercept_basic",
            "slope_intercept_modified",
            "dda_algorithm",
            "bresenham_real",
            "bresenham_integer"
        ]
        ttk.Label(self, text="Algoritmo:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.algo_var = tk.StringVar(value=algos[0])
        combo = ttk.Combobox(self, textvariable=self.algo_var, values=algos, state="readonly")
        combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Botones de control
        ttk.Button(self, text="Limpiar", command=self.clear).grid(row=0, column=2, padx=5)
        ttk.Button(self, text="Coordenadas", command=self.show_coords).grid(row=0, column=3, padx=5)

        # Canvas de dibujo
        self.canvas = tk.Canvas(self, bg="white", width=800, height=500, bd=2, relief="sunken")
        self.canvas.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_click)

        # Panel de información
        self.info = tk.Text(self, height=8, width=100)
        self.info.grid(row=2, column=0, columnspan=4, padx=10, pady=5)
        self.info.insert("end", "1) Clic: punto inicial\n2) Clic: punto final\n")

        self.grid()

    def on_click(self, event):
        x, y = event.x, event.y
        if self.start is None:
            self.start = (x, y)
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="green")
            self.info.insert("end", f"Inicio: {self.start}\n")
        else:
            self.end = (x, y)
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="red")
            self.info.insert("end", f"Fin: {self.end}\n")
            algo = self.algo_var.get()
            points = self.draw_callback(self.start, self.end, algo)
            for px, py in points:
                self.canvas.create_rectangle(px, py, px+1, py+1, fill="blue", outline="blue")
            self.info.insert("end", f"{algo}: {len(points)} puntos\n\n")
            # Preparar para nuevo
            self.start = None
            self.end = None

    def clear(self):
        self.canvas.delete("all")
        self.info.delete("1.0", "end")
        self.start = self.end = None
        self.info.insert("end", "Canvas limpio. Empieza de nuevo.\n")

    def show_coords(self):
        msg = f"Inicio: {self.start}\nFin: {self.end}"
        messagebox.showinfo("Coordenadas actuales", msg)
