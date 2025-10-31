# gui_p2.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple, Callable
from transformations import (compose, translate, rotate_deg, scale, shear,
                             reflect_x, reflect_y, reflect_through_origin_line,
                             reflect_through_arbitrary_line, apply)

Point = Tuple[float, float]
Segment = Tuple[Point, Point]

class LineAndTransformGUI(ttk.Frame):
    def __init__(self, parent, draw_callback: Callable[[Point, Point, str], List[Point]]):
        super().__init__(parent)
        self.parent = parent
        self.draw_callback = draw_callback
        self.parent.title("Algoritmos de Línea + Transformaciones 2D (P1+P2)")
        self.parent.geometry("1100x760")
        self.start = None
        self.end = None
        self.dragging = False
        self.preview_ids = []
        self.figure: List[Segment] = []  # lista de segmentos guardados
        self._build_ui()
        self.grid()

    def _build_ui(self):
        # Layout principal
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        main = ttk.Frame(self)
        main.grid(row=0, column=0, sticky="nsew")
        main.columnconfigure(0, weight=0)
        main.columnconfigure(1, weight=1)
        main.columnconfigure(2, weight=0)

        # Panel izquierdo: controles de dibujo (heredados P1)
        left = ttk.Frame(main)
        left.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        ttk.Label(left, text="Algoritmo de línea:").pack(anchor="w")
        self.algos = ["slope_intercept_basic","slope_intercept_modified",
                      "dda_algorithm","bresenham_real","bresenham_integer"]
        self.algo_var = tk.StringVar(value=self.algos[0])
        ttk.Combobox(left, textvariable=self.algo_var, values=self.algos, state="readonly").pack(fill="x")

        self.auto_add = tk.BooleanVar(value=True)
        ttk.Checkbutton(left, text="Añadir automáticamente a figura", variable=self.auto_add).pack(anchor="w", pady=4)

        ttk.Button(left, text="Limpiar canvas", command=self.clear_canvas).pack(fill="x", pady=4)
        ttk.Button(left, text="Vaciar figura", command=self.clear_figure).pack(fill="x", pady=4)
        ttk.Button(left, text="Añadir último segmento", command=self.add_last_segment).pack(fill="x", pady=4)

        # Canvas al centro
        self.canvas = tk.Canvas(main, bg="white", width=750, height=700, bd=2, relief="sunken")
        self.canvas.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Panel derecho: Transformaciones (P2)
        right = ttk.LabelFrame(main, text="Transformaciones 2D (matrices)")
        right.grid(row=0, column=2, padx=10, pady=10, sticky="ns")

        # Traslación
        ttk.Label(right, text="Traslación tx, ty").pack(anchor="w")
        self.tx = tk.DoubleVar(value=0.0); self.ty = tk.DoubleVar(value=0.0)
        ttk.Entry(right, textvariable=self.tx, width=8).pack(side="left", padx=2)
        ttk.Entry(right, textvariable=self.ty, width=8).pack(side="left", padx=2)
        ttk.Label(right, text=" ").pack()  # salto

        # Rotación y Escala
        f1 = ttk.Frame(right); f1.pack(fill="x", pady=4)
        ttk.Label(f1, text="Rotación θ°").grid(row=0, column=0, sticky="w")
        self.angle = tk.DoubleVar(value=0.0)
        ttk.Entry(f1, textvariable=self.angle, width=8).grid(row=0, column=1, padx=4)

        ttk.Label(f1, text="Escala sx, sy").grid(row=1, column=0, sticky="w")
        self.sx = tk.DoubleVar(value=1.0); self.sy = tk.DoubleVar(value=1.0)
        ttk.Entry(f1, textvariable=self.sx, width=8).grid(row=1, column=1, padx=4, sticky="w")
        ttk.Entry(f1, textvariable=self.sy, width=8).grid(row=1, column=2, padx=4, sticky="w")

        # Cizalla
        f2 = ttk.Frame(right); f2.pack(fill="x", pady=4)
        ttk.Label(f2, text="Cizalla shx, shy").grid(row=0, column=0, sticky="w")
        self.shx = tk.DoubleVar(value=0.0); self.shy = tk.DoubleVar(value=0.0)
        ttk.Entry(f2, textvariable=self.shx, width=8).grid(row=0, column=1, padx=4)
        ttk.Entry(f2, textvariable=self.shy, width=8).grid(row=0, column=2, padx=4)

        # Reflexiones
        ttk.Separator(right).pack(fill="x", pady=6)
        ttk.Label(right, text="Reflexión").pack(anchor="w")
        self.ref_mode = tk.StringVar(value="none")
        for txt,val in [("Ninguna","none"),("Eje X","x"),("Eje Y","y"),
                        ("Recta por origen (θ)","origin"),
                        ("Recta arbitraria (θ, px, py)","arbitrary")]:
            ttk.Radiobutton(right, text=txt, variable=self.ref_mode, value=val).pack(anchor="w")

        f3 = ttk.Frame(right); f3.pack(fill="x", pady=2)
        ttk.Label(f3, text="θ°").grid(row=0, column=0, sticky="e")
        self.theta = tk.DoubleVar(value=0.0)
        ttk.Entry(f3, textvariable=self.theta, width=8).grid(row=0, column=1, padx=4)

        f4 = ttk.Frame(right); f4.pack(fill="x", pady=2)
        ttk.Label(f4, text="px, py").grid(row=0, column=0, sticky="e")
        self.px = tk.DoubleVar(value=0.0); self.py = tk.DoubleVar(value=0.0)
        ttk.Entry(f4, textvariable=self.px, width=8).grid(row=0, column=1, padx=4)
        ttk.Entry(f4, textvariable=self.py, width=8).grid(row=0, column=2, padx=4)

        ttk.Separator(right).pack(fill="x", pady=6)
        ttk.Button(right, text="Vista previa", command=self.preview_transform).pack(fill="x", pady=2)
        ttk.Button(right, text="Aplicar a la figura", command=self.apply_transform).pack(fill="x", pady=2)
        ttk.Button(right, text="Reset figura", command=self.reset_figure).pack(fill="x", pady=8)

        # Info
        self.info = tk.Text(self, height=6, width=100)
        self.info.grid(row=1, column=0, padx=10, pady=(0,10), sticky="ew", columnspan=1)
        self.info.insert("end","1) Clic define inicio, arrastra para vista previa, suelta para fijar el segmento.\n")
        self.info.insert("end","2) Marca 'Añadir automáticamente' para ir construyendo la figura.\n")

    # ---- Dibujo interactivo (P1) ----
    def clear_canvas(self):
        self.canvas.delete("all")
        self.preview_ids.clear()
        self.info.insert("end","Canvas limpiado.\n")

    def clear_figure(self):
        self.figure.clear()
        self.info.insert("end","Figura vaciada.\n")
        self.redraw_figure()

    def add_last_segment(self):
        if self.start is None and self.end is None and hasattr(self, "last_seg"):
            self.figure.append(self.last_seg)
            self.info.insert("end",f"Añadido segmento {self.last_seg} a la figura.\n")
            self.redraw_figure()

    def on_click(self, event):
        self.start = (event.x, event.y)
        self.end = None
        self.dragging = True

    def on_drag(self, event):
        if not self.dragging or self.start is None:
            return
        self.end = (event.x, event.y)
        self._draw_preview(self.start, self.end)

    def on_release(self, event):
        if not self.dragging or self.start is None:
            return
        self.dragging = False
        self.end = (event.x, event.y)
        self._draw_segment(self.start, self.end)  # traza definitivo con el algoritmo elegido
        self.last_seg = (self.start, self.end)
        if self.auto_add.get():
            self.figure.append(self.last_seg)
            self.redraw_figure()
        self.start, self.end = None, None

    def _draw_preview(self, p0: Point, p1: Point):
        for oid in self.preview_ids:
            self.canvas.delete(oid)
        self.preview_ids.clear()
        pts = self.draw_callback(p0, p1, self.algo_var.get())
        for (x,y) in pts:
            oid = self.canvas.create_rectangle(x, y, x+1, y+1, fill="#888", outline="#888")
            self.preview_ids.append(oid)

    def _draw_segment(self, p0: Point, p1: Point):
        pts = self.draw_callback(p0, p1, self.algo_var.get())
        for (x,y) in pts:
            self.canvas.create_rectangle(x, y, x+1, y+1, fill="blue", outline="blue")

    def redraw_figure(self, preview: List[Segment]=None):
        self.canvas.delete("all")
        segs = preview if preview is not None else self.figure
        for (a,b) in segs:
            self._draw_segment(a,b)

    # ---- Transformaciones (P2) ----
    def _current_matrix(self):
        M = compose(translate(self.tx.get(), self.ty.get()),
                    rotate_deg(self.angle.get()),
                    scale(self.sx.get(), self.sy.get()),
                    shear(self.shx.get(), self.shy.get()))
        mode = self.ref_mode.get()
        if mode == "x":
            M = compose(M, reflect_x())
        elif mode == "y":
            M = compose(M, reflect_y())
        elif mode == "origin":
            M = compose(M, reflect_through_origin_line(self.theta.get()))
        elif mode == "arbitrary":
            M = compose(M, reflect_through_arbitrary_line(self.px.get(), self.py.get(), self.theta.get()))
        return M

    def preview_transform(self):
        if not self.figure:
            messagebox.showwarning("Aviso","No hay segmentos en la figura.")
            return
        M = self._current_matrix()
        segs = [ (apply(M,[a])[0], apply(M,[b])[0]) for (a,b) in self.figure ]
        self.redraw_figure(preview=segs)

    def apply_transform(self):
        if not self.figure:
            messagebox.showwarning("Aviso","No hay segmentos en la figura.")
            return
        M = self._current_matrix()
        self.figure = [ (apply(M,[a])[0], apply(M,[b])[0]) for (a,b) in self.figure ]
        self.redraw_figure()
        self.info.insert("end","Transformación aplicada a la figura.\n")

    def reset_figure(self):
        self.figure.clear()
        self.clear_canvas()
        self.info.insert("end","Figura reiniciada.\n")
