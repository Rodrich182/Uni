import tkinter as tk
from tkinter import ttk, messagebox

class LineDrawingGUI(ttk.Frame):
    def __init__(self, parent, draw_callback):
        super().__init__(parent)
        self.parent = parent
        self.draw_callback = draw_callback
        self.parent.title("Visualizador de Algoritmos de Línea")
        self.parent.geometry("900x700")
        self.start = None
        self.end = None
        self.last_start = None
        self.last_end = None

        algos = [
            "slope_intercept_basic",
            "slope_intercept_modified",
            "dda_algorithm",
            "bresenham_real",
            "bresenham_integer"
        ]

        # Canvas de dibujo a la izquierda
        self.canvas = tk.Canvas(self, bg="white", width=500, height=500, bd=2, relief="sunken")
        self.canvas.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        self.canvas.bind("<Button-1>", self.on_click)

        # --- Panel de controles a la derecha (vertical) ---
        controles = ttk.Frame(self)
        controles.grid(row=0, column=1, padx=20, pady=10, sticky="n")
        
        # Label y selector en la misma fila del panel de controles
        ttk.Label(controles, text="Algoritmo:").grid(row=0, column=0, padx=(0,5), pady=5, sticky="e")
        self.algo_var = tk.StringVar(value=algos[0])
        ttk.Combobox(controles, textvariable=self.algo_var, values=algos, state="readonly").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        # Botones ambos abajo
        ttk.Button(controles, text="Limpiar", command=self.clear).grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        ttk.Button(controles, text="Coordenadas", command=self.show_coords).grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

        # Panel de información abajo (ocupa dos columnas)
        self.info = tk.Text(self, height=10, width=100)
        self.info.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.info.insert("end", "1) Clic: punto inicial\n2) Clic: punto final\n")

        self.grid()

    def clear(self):
        self.canvas.delete("all")
        self.info.delete("1.0", "end")
        self.start = None
        self.end = None
        self.last_start = None
        self.last_end = None
        self.info.insert("end", "Canvas limpio. Empieza de nuevo.\n")

    def on_click(self, event):
        x, y = event.x, event.y
        if self.start is None:
            self.start = (x, y)
            self.end = None
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
            self.last_start = self.start
            self.last_end = self.end
            self.start = None
            self.end = None

    def show_coords(self):
        if self.start is not None and self.end is None:
            msg = f"Inicio: {self.start}\nFin: None"
        elif self.last_start is not None and self.last_end is not None:
            msg = f"Inicio: {self.last_start}\nFin: {self.last_end}"
        else:
            msg = "Inicio: None\nFin: None"
        messagebox.showinfo("Coordenadas actuales", msg)
