
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import dictionary as D

from transformations.compose import apply_all
from animations.gif_export import export_gif

class Practica2Panel(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.vertices = []   # lista de (x,y) enteros
        self.closed = False  # figura cerrada
        self.mode_var = tk.StringVar(value="dibujo")  # 'dibujo' | 'vertices' | 'segmentos'

        # Modo de creación
        ttk.Label(self, text="Creación de figura:").grid(row=0, column=0, sticky="w", pady=(0,4))
        for i,(k,txt) in enumerate([("dibujo","Dibujo por clics"),
                                    ("vertices","Vértices (x,y)"),
                                    ("segmentos","Segmentos (x1,y1;x2,y2)")]):
            ttk.Radiobutton(self, text=txt, value=k, variable=self.mode_var, command=self._on_mode_change).grid(row=1, column=i, padx=4, sticky="w")

        # Área de entrada (para vertices/segmentos)
        self.txt = tk.Text(self, width=42, height=8, bg=self.app.palette["text_bg"], fg=self.app.palette["text_fg"])
        self.txt.grid(row=2, column=0, columnspan=3, pady=4, sticky="ew")
        self.txt.configure(state="disabled")

        # Botones figura
        btns = ttk.Frame(self); btns.grid(row=3, column=0, columnspan=3, pady=6, sticky="ew")
        ttk.Button(btns, text="Cargar entrada", command=self.load_from_text).grid(row=0, column=0, padx=3)
        ttk.Button(btns, text="Cerrar figura", command=self.close_shape).grid(row=0, column=1, padx=3)
        ttk.Button(btns, text="Limpiar figura", command=self.clear_shape).grid(row=0, column=2, padx=3)

        # Parámetros de transformaciones
        row = 4
        ttk.Label(self, text="Transformaciones (orden fijo): T → R → S → Reflexiones → Cizalla").grid(row=row, column=0, columnspan=3, sticky="w", pady=(8,4))
        row += 1

        # Traslación
        ttk.Label(self, text="Traslación tx, ty:").grid(row=row, column=0, sticky="e"); 
        self.tx = tk.IntVar(value=0); self.ty = tk.IntVar(value=0)
        ttk.Entry(self, textvariable=self.tx, width=6).grid(row=row, column=1, sticky="w", padx=2)
        ttk.Entry(self, textvariable=self.ty, width=6).grid(row=row, column=2, sticky="w", padx=2); row += 1

        # Rotación
        ttk.Label(self, text="Rotación θ (deg):").grid(row=row, column=0, sticky="e")
        self.rot = tk.DoubleVar(value=0.0)
        ttk.Entry(self, textvariable=self.rot, width=6).grid(row=row, column=1, sticky="w", padx=2); row += 1

        # Escalado
        ttk.Label(self, text="Escalado sx, sy:").grid(row=row, column=0, sticky="e")
        self.sx = tk.DoubleVar(value=1.0); self.sy = tk.DoubleVar(value=1.0)
        ttk.Entry(self, textvariable=self.sx, width=6).grid(row=row, column=1, sticky="w", padx=2)
        ttk.Entry(self, textvariable=self.sy, width=6).grid(row=row, column=2, sticky="w", padx=2); row += 1

        # Reflexiones básicas
        self.refl_x = tk.BooleanVar(value=False); self.refl_y = tk.BooleanVar(value=False)
        ttk.Checkbutton(self, text="Reflexión eje X", variable=self.refl_x).grid(row=row, column=0, sticky="w"); 
        ttk.Checkbutton(self, text="Reflexión eje Y", variable=self.refl_y).grid(row=row, column=1, sticky="w"); row += 1

        # Reflexión por recta que pasa por origen
        ttk.Label(self, text="Reflexión por recta (origen) θ (deg):").grid(row=row, column=0, sticky="e")
        self.refl_theta = tk.DoubleVar(value=0.0)
        ttk.Entry(self, textvariable=self.refl_theta, width=6).grid(row=row, column=1, sticky="w", padx=2); row += 1

        # Reflexión por recta arbitraria ax + by + c = 0
        ttk.Label(self, text="Reflexión por recta arbitraria a,b,c:").grid(row=row, column=0, sticky="e")
        self.ra = tk.DoubleVar(value=0.0); self.rb = tk.DoubleVar(value=0.0); self.rc = tk.DoubleVar(value=0.0)
        ttk.Entry(self, textvariable=self.ra, width=6).grid(row=row, column=1, sticky="w", padx=2)
        ttk.Entry(self, textvariable=self.rb, width=6).grid(row=row, column=2, sticky="w", padx=2)
        ttk.Entry(self, textvariable=self.rc, width=6).grid(row=row, column=3, sticky="w", padx=2); row += 1

        # Cizalla
        ttk.Label(self, text="Cizalla shx, shy:").grid(row=row, column=0, sticky="e")
        self.shx = tk.DoubleVar(value=0.0); self.shy = tk.DoubleVar(value=0.0)
        ttk.Entry(self, textvariable=self.shx, width=6).grid(row=row, column=1, sticky="w", padx=2)
        ttk.Entry(self, textvariable=self.shy, width=6).grid(row=row, column=2, sticky="w", padx=2); row += 1

        # Acciones de transformación y animación
        ttk.Button(self, text="Aplicar cambios", command=self.apply_changes).grid(row=row, column=0, columnspan=2, sticky="ew", pady=8)
        ttk.Button(self, text="Generar animación (GIF)", command=self.make_gif).grid(row=row, column=2, columnspan=2, sticky="ew", pady=8)

        # Integración de eventos del canvas (solo en modo dibujo)
        self.app.canvas.bind("<Button-1>", self._on_canvas_click)
        self._overlay_tag = "p2_overlay"

    def _on_mode_change(self):
        mode = self.mode_var.get()
        if mode == "dibujo":
            self.txt.configure(state="disabled")
        else:
            self.txt.configure(state="normal")

    def _on_canvas_click(self, event):
        if self.mode_var.get() != "dibujo":
            return
        gx, gy = self.app.screen_to_grid(event.x, event.y)
        self.vertices.append((gx, gy))
        self._redraw_figure()

    def load_from_text(self):
        try:
            text = self.txt.get("1.0", "end").strip()
            if not text:
                return
            verts = []
            segs = []
            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue
                if self.mode_var.get() == "vertices":
                    # Formato: x y  o  x,y
                    parts = line.replace(",", " ").split()
                    if len(parts) != 2: 
                        raise ValueError("Formato de vértice inválido")
                    x, y = int(float(parts[0])), int(float(parts[1]))
                    verts.append((x, y))
                else:
                    # segmentos: x1,y1;x2,y2
                    L = line.split(";")
                    if len(L) != 2: 
                        raise ValueError("Formato de segmento inválido")
                    def parse_pair(s):
                        p = s.replace(",", " ").split()
                        if len(p) != 2: 
                            raise ValueError("Par inválido")
                        return (int(float(p[0])), int(float(p[1])))
                    p1 = parse_pair(L[0]); p2 = parse_pair(L[1])
                    segs.append((p1, p2))
            if self.mode_var.get() == "vertices":
                self.vertices = verts
                self.closed = False
            else:
                # Convertir segmentos a lista de vértices ordenada conectando en cadena si posible
                self.vertices = [segs[0][0], segs[0][1]]
                for (a,b) in segs[1:]:
                    if self.vertices[-1] == a:
                        self.vertices.append(b)
                    elif self.vertices[-1] == b:
                        self.vertices.append(a)
                    else:
                        self.vertices.append(a)
                        self.vertices.append(b)
                self.closed = False
            self._redraw_figure()
        except Exception as e:
            messagebox.showerror("Error de entrada", str(e))

    def close_shape(self):
        if len(self.vertices) >= 3:
            self.closed = True
            self._redraw_figure()

    def clear_shape(self):
        self.vertices.clear()
        self.closed = False
        self.app.canvas.delete(self._overlay_tag)
        self.app.clear()

    def apply_changes(self):
        if not self.vertices:
            messagebox.showwarning("Figura vacía", "Primero crea o carga una figura")
            return
        params = {
            'tx': self.tx.get(), 'ty': self.ty.get(),
            'rot': self.rot.get(),
            'sx': self.sx.get(), 'sy': self.sy.get(),
            'refl_x': self.refl_x.get(), 'refl_y': self.refl_y.get(),
            'refl_theta': self.refl_theta.get(),
            'refl_a': self.ra.get(), 'refl_b': self.rb.get(), 'refl_c': self.rc.get(),
            'shx': self.shx.get(), 'shy': self.shy.get(),
        }
        new_vertices, seq = apply_all(self.vertices, params)
        self.vertices = new_vertices
        self._redraw_figure()
        self.app.info.insert("end", f"Aplicadas {len(seq)} transformaciones.\n")

    def make_gif(self):
        if not self.vertices:
            messagebox.showwarning("Figura vacía", "Primero crea o carga una figura")
            return
        from PIL import Image  # comprobar disponibilidad
        path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF animado",".gif")], title="Guardar animación")
        if not path:
            return
        params = {
            'tx': self.tx.get(), 'ty': self.ty.get(),
            'rot': self.rot.get(),
            'sx': self.sx.get(), 'sy': self.sy.get(),
            'refl_x': self.refl_x.get(), 'refl_y': self.refl_y.get(),
            'refl_theta': self.refl_theta.get(),
            'refl_a': self.ra.get(), 'refl_b': self.rb.get(), 'refl_c': self.rc.get(),
            'shx': self.shx.get(), 'shy': self.shy.get(),
        }
        out = export_gif(
            self.vertices, self.closed, params,
            canvas_size=self.app.canvas_size, pixel_size=D.SETTINGS.get("pixel_size", 8),
            palette=self.app.palette, steps_per_op=20, out_path=path, duration_ms=30
        )
        messagebox.showinfo("Animación creada", f"Guardado en: {out}")

    def _redraw_figure(self):
        # Limpiar canvas (framebuffer) y overlay
        self.app._rebuild_framebuffer()
        self.app.canvas.delete("axes")
        self.app.draw_axes()
        self.app.canvas.delete(self._overlay_tag)

        # Dibujar aristas con rasterización actual
        if len(self.vertices) >= 2:
            pairs = list(zip(self.vertices, self.vertices[1:]))
            if self.closed:
                pairs.append((self.vertices[-1], self.vertices[0]))
            for (x1,y1),(x2,y2) in pairs:
                pts = self.app.draw_callback((x1,y1), (x2,y2), D.SETTINGS["active_line_algorithm"])
                for (px, py) in pts:
                    self.app._put_pixel(px, py)

        # Dibujar vértices y coordenadas como overlay vectorial
        for (x, y) in self.vertices:
            sx = self.app.center_x + x * D.SETTINGS.get("pixel_size", 8)
            sy = self.app.center_y - y * D.SETTINGS.get("pixel_size", 8)
            r = max(2, D.SETTINGS.get("pixel_size", 8)//2)
            self.app.canvas.create_oval(sx-r, sy-r, sx+r, sy+r, fill=self.app.palette["line_color"], outline="", tags=self._overlay_tag)
            self.app.canvas.create_text(sx + 10, sy - 10, text=f"({x},{y})", fill=self.app.palette["line_color"], anchor="w", tags=self._overlay_tag)

        self.app._refresh_image()