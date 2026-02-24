import tkinter as tk
from tkinter import ttk, messagebox

import dictionary as D
from fractals import (
    sierpinski_segments,
    koch_segments,
    mandelbrot_points,
    julia_points,
    barnsley_points,
    sierpinski_ifs_points,
)


class Practica3Panel(ttk.Frame):
    """
    Práctica 3: Fractales
    - Fractales recursivos (Sierpinski / Koch)
    - Conjunto de Mandelbrot
    - Conjuntos de Julia
    - IFS (Barnsley / Sierpinski IFS)
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # ---------- Estado ----------
        self.recursive_type = tk.StringVar(
            value=D.DEFAULT_FRACTAL_RECURSIVE
        )
        self.recursive_level = tk.IntVar(
            value=D.DEFAULT_FRACTAL_LEVEL
        )

        self.mandel_max_iter = tk.IntVar(
            value=D.DEFAULT_FRACTAL_ITER
        )

        self.julia_max_iter = tk.IntVar(
            value=D.DEFAULT_FRACTAL_ITER
        )
        self.julia_cre = tk.DoubleVar(value=-0.8)
        self.julia_cim = tk.DoubleVar(value=0.156)

        self.ifs_type = tk.StringVar(
            value=D.DEFAULT_FRACTAL_IFS
        )
        self.ifs_iter = tk.IntVar(
            value=D.DEFAULT_IFS_ITER
        )
        self.ifs_skip = tk.IntVar(
            value=D.DEFAULT_IFS_SKIP
        )

        # Construir la interfaz
        self._build_ui()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _build_ui(self):
        """
        Cuatro bloques de controles:
        - Fractal recursivo
        - Mandelbrot
        - Julia
        - IFS
        """
        # Fractal recursivo
        frame_rec = ttk.LabelFrame(self, text="Fractal recursivo")
        frame_rec.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        ttk.Label(frame_rec, text="Tipo:").grid(row=0, column=0, sticky="e")
        # Tipo de fractal recursivo
        ttk.Combobox(
            frame_rec,
            textvariable=self.recursive_type,
            values=D.FRACTAL_RECURSIVE_TYPES,
            state="readonly",
            width=15,
        ).grid(row=0, column=1, sticky="w", padx=3)
        # Nivel de recursión
        ttk.Label(frame_rec, text="Nivel de recursión:").grid(
            row=0, column=2, sticky="e", padx=6
        )
        tk.Spinbox(
            frame_rec,
            from_=0,
            to=10,
            textvariable=self.recursive_level,
            width=5,
        ).grid(row=0, column=3, sticky="w")
        # Botón de dibujo
        ttk.Button(
            frame_rec,
            text="Dibujar recursivo",
            command=self.on_draw_recursive,
        ).grid(row=0, column=4, padx=8)

        # Mandelbrot
        frame_man = ttk.LabelFrame(self, text="Conjunto de Mandelbrot")
        frame_man.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        # Iteraciones máximas
        ttk.Label(frame_man, text="Iteraciones máximas:").grid(
            row=0, column=0, sticky="e"
        )
        tk.Spinbox(
            frame_man,
            from_=10,
            to=1000,
            increment=10,
            textvariable=self.mandel_max_iter,
            width=6,
        ).grid(row=0, column=1, sticky="w", padx=3)
        # Botón de dibujo
        ttk.Button(
            frame_man,
            text="Dibujar Mandelbrot",
            command=self.on_draw_mandelbrot,
        ).grid(row=0, column=2, padx=8)

        # Julia 
        frame_julia = ttk.LabelFrame(self, text="Conjunto de Julia")
        frame_julia.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        # Parámetros de c
        ttk.Label(frame_julia, text="Re(c):").grid(row=0, column=0, sticky="e")
        ttk.Entry(frame_julia, textvariable=self.julia_cre, width=8).grid(
            row=0, column=1, sticky="w", padx=2
        )
        
        ttk.Label(frame_julia, text="Im(c):").grid(row=0, column=2, sticky="e")
        ttk.Entry(frame_julia, textvariable=self.julia_cim, width=8).grid(
            row=0, column=3, sticky="w", padx=2
        )
        # Iteraciones máximas
        ttk.Label(frame_julia, text="Iter. máx.:").grid(
            row=0, column=4, sticky="e", padx=4
        )
        tk.Spinbox(
            frame_julia,
            from_=10,
            to=1000,
            increment=10,
            textvariable=self.julia_max_iter,
            width=6,
        ).grid(row=0, column=5, sticky="w")
        # Botón de dibujo
        ttk.Button(
            frame_julia,
            text="Dibujar Julia",
            command=self.on_draw_julia,
        ).grid(row=0, column=6, padx=8)

        # IFS   
        frame_ifs = ttk.LabelFrame(self, text="Fractal con IFS (juego del caos)")
        frame_ifs.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        # Tipo de IFS
        ttk.Label(frame_ifs, text="Tipo IFS:").grid(row=0, column=0, sticky="e")
        ttk.Combobox(
            frame_ifs,
            textvariable=self.ifs_type,
            values=D.FRACTAL_IFS_TYPES,
            state="readonly",
            width=15,
        ).grid(row=0, column=1, sticky="w", padx=3)
        # Iteraciones
        ttk.Label(frame_ifs, text="Iteraciones:").grid(
            row=0, column=2, sticky="e", padx=4
        )
        ttk.Entry(frame_ifs, textvariable=self.ifs_iter, width=8).grid(
            row=0, column=3, sticky="w", padx=2
        )
        # Descartar primeras
        ttk.Label(frame_ifs, text="Descartar primeras:").grid(
            row=0, column=4, sticky="e", padx=4
        )
        ttk.Entry(frame_ifs, textvariable=self.ifs_skip, width=6).grid(
            row=0, column=5, sticky="w", padx=2
        )
        # Botón de dibujo
        ttk.Button(
            frame_ifs,
            text="Dibujar IFS",
            command=self.on_draw_ifs,
        ).grid(row=0, column=6, padx=8)

        # Que la columna 0 se expanda algo
        self.grid_columnconfigure(0, weight=1)

    # ------------------------------------------------------------------
    # Utilidades de dibujo
    # ------------------------------------------------------------------

    def _prepare_canvas(self, msg: str):
        """
        Limpia el framebuffer y ejes, y escribe un mensaje en el panel de info.
        """
        self.app.clear()
        try:
            self.app.info.insert("end", msg + "\n")
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Fractal recursivo (usa fractals.recursive)
    # ------------------------------------------------------------------

    def on_draw_recursive(self):
        """Dibuja un fractal recursivo (Sierpinski / Koch) en el canvas"""
        level = self.recursive_level.get()
        ftype = self.recursive_type.get()

        if level < 0:   # nivel inválido
            messagebox.showerror("Error", "El nivel de recursión debe ser >= 0.")
            return

        self._prepare_canvas(   
            f"Dibujando fractal recursivo '{ftype}' con nivel {level}..."  
        )

        size = min(self.app.grid_w, self.app.grid_h) // 2 # tamaño lógico

        if ftype == "sierpinski":
            segs = sierpinski_segments(level, size) # obtiene segmentos
        elif ftype == "koch":
            length = min(self.app.grid_w, self.app.grid_h) - 4
            segs = koch_segments(level, length) # obtiene segmentos
        else:
            messagebox.showerror("Error", f"Tipo recursivo desconocido: {ftype}")
            return

        algo = D.SETTINGS["active_line_algorithm"]  # algoritmo de línea

        for x1, y1, x2, y2 in segs:
            # Asegurar que los algoritmos de línea reciben enteros
            x1 = int(round(x1))     
            y1 = int(round(y1)) 
            x2 = int(round(x2)) 
            y2 = int(round(y2))

            pts = self.app.draw_callback((x1, y1), (x2, y2), algo)  # dibuja línea
            for px, py in pts:
                self.app._put_pixel(px, py)

        self.app._refresh_image()


    # ------------------------------------------------------------------
    # Mandelbrot (usa fractals.complex_sets)
    # ------------------------------------------------------------------

    def on_draw_mandelbrot(self):
        """Dibuja el conjunto de Mandelbrot en el canvas"""
        max_iter = self.mandel_max_iter.get()   
        if max_iter <= 0:   
            messagebox.showerror("Error", "Las iteraciones deben ser > 0.")
            return

        self._prepare_canvas(   
            f"Dibujando conjunto de Mandelbrot (iter máx = {max_iter})..."
        )

        w = self.app.grid_w 
        h = self.app.grid_h 
        xmin, xmax = -2.5, 1.5  
        ymin, ymax = -1.5, 1.5  

        pts = mandelbrot_points(w, h, xmin, xmax, ymin, ymax, max_iter) # obtiene puntos

        for gx, gy, n in pts:
            if n == max_iter:   
                color = "#000000"
            else:
                shade = int(255 * n / max_iter) 
                color = f"#{shade:02x}{shade:02x}{shade:02x}"   
            self.app._put_pixel(gx, gy, color)  

        self.app._refresh_image()   # actualiza el canvas

    # ------------------------------------------------------------------
    # Julia (usa fractals.complex_sets)
    # ------------------------------------------------------------------

    def on_draw_julia(self):
        """Dibuja el conjunto de Julia en el canvas"""
        max_iter = self.julia_max_iter.get()    
        if max_iter <= 0:
            messagebox.showerror("Error", "Las iteraciones deben ser > 0.")
            return

        cre = self.julia_cre.get()  
        cim = self.julia_cim.get()  
        c = complex(cre, cim)

        self._prepare_canvas(
            f"Dibujando conjunto de Julia para c = {cre} + {cim}i (iter máx = {max_iter})..."
        )   

        w = self.app.grid_w 
        h = self.app.grid_h
        xmin, xmax = -1.5, 1.5
        ymin, ymax = -1.5, 1.5

        pts = julia_points(w, h, xmin, xmax, ymin, ymax, c, max_iter)

        for gx, gy, n in pts:
            if n == max_iter:
                color = "#000000"
            else:
                shade = int(255 * n / max_iter) 
                color = f"#{shade:02x}{shade:02x}{shade:02x}"
            self.app._put_pixel(gx, gy, color)  

        self.app._refresh_image()   

    # ------------------------------------------------------------------
    # IFS (usa fractals.ifs)
    # ------------------------------------------------------------------

    def on_draw_ifs(self):
        """Dibuja un fractal usando IFS en el canvas"""
        ftype = self.ifs_type.get()
        iters = self.ifs_iter.get()
        skip = self.ifs_skip.get()

        if iters <= 0:
            messagebox.showerror("Error", "Las iteraciones deben ser > 0.")
            return
        if skip < 0 or skip >= iters:
            messagebox.showerror(
                "Error",
                "El número de iteraciones a descartar debe ser >= 0 y < iteraciones.",
            )
            return

        self._prepare_canvas(
            f"Dibujando IFS '{ftype}' con {iters} iteraciones (descartando {skip})..."
        )

        w = self.app.grid_w
        h = self.app.grid_h

        if ftype == "barnsley":
            pts = barnsley_points(w, h, iters, skip)
            color = "#008000"
        elif ftype == "sierpinski_ifs":
            pts = sierpinski_ifs_points(w, h, iters, skip)
            color = "#0000ff"
        else:
            messagebox.showerror("Error", f"Tipo IFS desconocido: {ftype}")
            return

        for gx, gy in pts:
            self.app._put_pixel(gx, gy, color)

        self.app._refresh_image()
