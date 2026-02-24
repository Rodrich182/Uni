# gui/practicas/practica2.py

import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from animations.runtime import iter_frames_vertices
import dictionary as D
from animations.gif_export import export_gif
from transformations.compose import apply_all, build_matrix_sequence
from transformations.matrices import (
    apply_matrix_to_points,
    T as Tm,
    R_deg as Rm,
    S as Sm,
    shear as ShearM,
)


class Practica2Panel(ttk.Frame):
    """
    Editor de figura y animación de transformaciones 2D:
    T, R, S, reflexiones (X, Y, recta por origen, recta arbitraria) y cizalla.
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Estado de la figura
        self.vertices = []          # lista de (x,y) enteros
        self.closed = False         # figura cerrada
        self.mode_var = tk.StringVar(value="dibujo")  # 'dibujo' | 'vertices' | 'segmentos'
        self._overlay_tag = "p2_overlay"

        # ---------- UI: creación ----------
        ttk.Label(self, text="Creación de figura:").grid(row=0, column=0, sticky="w", pady=(0, 4))
        for i, (k, txt) in enumerate([
            ("dibujo", "Dibujo por clics"),
            ("vertices", "Vértices (x,y)"),
            ("segmentos", "Segmentos (x1,y1;x2,y2)")
        ]):
            ttk.Radiobutton(
                self, text=txt, value=k, variable=self.mode_var, command=self._on_mode_change
            ).grid(row=1, column=i, padx=4, sticky="w")

        # Área de texto para entrada manual (vértices o segmentos)
        self.txt = tk.Text(
            self, width=42, height=8,
            bg=self.app.palette.get("text_bg", "white"),
            fg=self.app.palette.get("text_fg", "black")
        )
        self.txt.grid(row=2, column=0, columnspan=4, pady=4, sticky="ew")
        self.txt.configure(state="disabled")

        # Botones de figura
        btns = ttk.Frame(self)
        btns.grid(row=3, column=0, columnspan=4, pady=6, sticky="ew")
        ttk.Button(btns, text="Cargar entrada", command=self.load_from_text).grid(row=0, column=0, padx=3)
        ttk.Button(btns, text="Cerrar figura", command=self.close_shape).grid(row=0, column=1, padx=3)
        ttk.Button(btns, text="Limpiar figura", command=self.clear_shape).grid(row=0, column=2, padx=3)

        # ---------- UI: transformaciones ----------
        row = 4
        ttk.Label(self, text="Transformaciones (orden fijo): T → R → S → Reflexiones → Cizalla").grid(
            row=row, column=0, columnspan=4, sticky="w", pady=(8, 4)
        )
        row += 1

        # Traslación
        ttk.Label(self, text="Traslación tx, ty:").grid(row=row, column=0, sticky="e")
        self.tx = tk.IntVar(value=0)
        self.ty = tk.IntVar(value=0)
        ttk.Entry(self, textvariable=self.tx, width=6).grid(row=row, column=1, sticky="w", padx=2)
        ttk.Entry(self, textvariable=self.ty, width=6).grid(row=row, column=2, sticky="w", padx=2)
        row += 1

        # Rotación
        ttk.Label(self, text="Rotación θ (deg):").grid(row=row, column=0, sticky="e")
        self.rot = tk.DoubleVar(value=0.0)
        ttk.Entry(self, textvariable=self.rot, width=6).grid(row=row, column=1, sticky="w", padx=2)
        row += 1

        # Escalado
        ttk.Label(self, text="Escalado sx, sy:").grid(row=row, column=0, sticky="e")
        self.sx = tk.DoubleVar(value=1.0)
        self.sy = tk.DoubleVar(value=1.0)
        ttk.Entry(self, textvariable=self.sx, width=6).grid(row=row, column=1, sticky="w", padx=2)
        ttk.Entry(self, textvariable=self.sy, width=6).grid(row=row, column=2, sticky="w", padx=2)
        row += 1

        # Reflexiones básicas
        self.refl_x = tk.BooleanVar(value=False)
        self.refl_y = tk.BooleanVar(value=False)
        ttk.Checkbutton(self, text="Reflexión eje X", variable=self.refl_x).grid(row=row, column=0, sticky="w")
        ttk.Checkbutton(self, text="Reflexión eje Y", variable=self.refl_y).grid(row=row, column=1, sticky="w")
        row += 1

        # Reflexión por recta que pasa por el origen (ángulo θ)
        ttk.Label(self, text="Reflexión por recta (origen) θ (deg):").grid(row=row, column=0, sticky="e")
        self.refl_theta = tk.DoubleVar(value=0.0)
        ttk.Entry(self, textvariable=self.refl_theta, width=6).grid(row=row, column=1, sticky="w", padx=2)
        row += 1

        # Reflexión por recta arbitraria ax + by + c = 0
        ttk.Label(self, text="Reflexión recta arbitraria a, b, c:").grid(row=row, column=0, sticky="e")
        self.ra = tk.DoubleVar(value=0.0)
        self.rb = tk.DoubleVar(value=0.0)
        self.rc = tk.DoubleVar(value=0.0)
        ttk.Entry(self, textvariable=self.ra, width=6).grid(row=row, column=1, sticky="w", padx=2)
        ttk.Entry(self, textvariable=self.rb, width=6).grid(row=row, column=2, sticky="w", padx=2)
        ttk.Entry(self, textvariable=self.rc, width=6).grid(row=row, column=3, sticky="w", padx=2)
        row += 1

        # Cizalla
        ttk.Label(self, text="Cizalla shx, shy:").grid(row=row, column=0, sticky="e")
        self.shx = tk.DoubleVar(value=0.0)
        self.shy = tk.DoubleVar(value=0.0)
        ttk.Entry(self, textvariable=self.shx, width=6).grid(row=row, column=1, sticky="w", padx=2)
        ttk.Entry(self, textvariable=self.shy, width=6).grid(row=row, column=2, sticky="w", padx=2)
        row += 1

        # Acciones
        ttk.Button(self, text="Aplicar cambios", command=self.apply_changes).grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=8
        )
        ttk.Button(self, text="Generar animación (GIF)", command=self.make_gif).grid(
            row=row, column=2, columnspan=2, sticky="ew", pady=8
        )
        ttk.Button(self, text="Animar y aplicar", command=self.animate_and_apply).grid(
            row=row + 1, column=0, columnspan=4, sticky="ew", pady=6
        )

        # Binding de canvas para modo "dibujo"
        self.app.canvas.bind("<Button-1>", self._on_canvas_click)

    # ---------- Entradas y figura ----------
    def _on_mode_change(self):
        """Maneja el cambio de modo de entrada."""
        if self.mode_var.get() == "dibujo":
            self.txt.configure(state="disabled")
        else:
            self.txt.configure(state="normal")

    def _on_canvas_click(self, event):
        """Maneja el clic en el canvas para añadir vértices en modo dibujo."""
        if self.mode_var.get() != "dibujo":
            return
        gx, gy = self.app.screen_to_grid(event.x, event.y)
        self.vertices.append((gx, gy))
        self._redraw_figure()

    def load_from_text(self):
        """Carga la figura desde el área de texto según el modo seleccionado."""
        try:
            text = self.txt.get("1.0", "end").strip()
            if not text:
                return

            if self.mode_var.get() == "vertices":
                verts = []
                for line in text.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.replace(",", " ").split()
                    if len(parts) != 2:
                        raise ValueError("Formato de vértice inválido (usa: x y)")
                    x, y = int(float(parts[0])), int(float(parts[1]))
                    verts.append((x, y))
                self.vertices = verts
                self.closed = False

            else:  # segmentos: "x1,y1;x2,y2" por línea
                segs = []
                for line in text.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    L = line.split(";")
                    if len(L) != 2:
                        raise ValueError("Formato de segmento inválido (usa: x1,y1;x2,y2)")
                    def parse_pair(s):
                        p = s.replace(",", " ").split()
                        if len(p) != 2:
                            raise ValueError("Par inválido (usa: x y)")
                        return int(float(p[0])), int(float(p[1]))
                    p1 = parse_pair(L[0]); p2 = parse_pair(L[1])
                    segs.append((p1, p2))

                # Reconstrucción sencilla de polyline conectando si coincide extremo
                self.vertices = [segs[0][0], segs[0][1]]
                for (a, b) in segs[1:]:
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
        """Cierra la figura conectando el último vértice con el primero."""
        if len(self.vertices) >= 3:
            self.closed = True
            self._redraw_figure()

    def clear_shape(self):
        """Limpia la figura actual."""
        self.vertices.clear()
        self.closed = False
        self.app.canvas.delete(self._overlay_tag)
        self.app.clear()

    # ---------- Transformaciones ----------
    def _collect_params(self):
        """Recopila los parámetros de transformación desde la UI."""
        return {
            "tx": self.tx.get(), "ty": self.ty.get(),
            "rot": self.rot.get(),
            "sx": self.sx.get(), "sy": self.sy.get(),
            "refl_x": self.refl_x.get(), "refl_y": self.refl_y.get(),
            "refl_theta": self.refl_theta.get(),
            "refl_a": self.ra.get(), "refl_b": self.rb.get(), "refl_c": self.rc.get(),
            "shx": self.shx.get(), "shy": self.shy.get(),
        }

    def apply_changes(self):
        """Aplica las transformaciones a la figura actual."""
        if not self.vertices:
            messagebox.showwarning("Figura vacía", "Primero crea o carga una figura")
            return
        params = self._collect_params()
        new_vertices, seq = apply_all(self.vertices, params)
        self.vertices = new_vertices
        self._redraw_figure()
        self.app.info.insert("end", f"Aplicadas {len(seq)} transformaciones.\n")

    def make_gif(self):
        """Genera una animación GIF de las transformaciones aplicadas."""
        if not self.vertices:
            messagebox.showwarning("Figura vacía", "Primero crea o carga una figura")
            return
        try:
            import PIL  # noqa: F401
        except Exception as e:
            messagebox.showerror("Dependencia faltante", "Instala Pillow: pip install Pillow\n\n" + str(e))
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".gif",
            filetypes=[("GIF animado", ".gif")],
            title="Guardar animación"
        )
        if not path:
            return

        params = self._collect_params()
        try:
            out = export_gif(
                self.vertices,
                self.closed,
                params,
                canvas_size=self.app.canvas_size,
                pixel_size=D.SETTINGS.get("pixel_size", 8),
                palette=self.app.palette,
                steps_per_op=20,
                out_path=path,
                duration_ms=50
            )
            messagebox.showinfo("Animación creada", f"Guardado en: {out}")
        except Exception as e:
            messagebox.showerror("Error al exportar GIF", str(e))

    # ---------- Dibujo en canvas ----------
    def _redraw_figure(self):
        """Redibuja la figura actual en el canvas."""
        # Limpiar framebuffer y ejes
        self.app._rebuild_framebuffer()
        self.app.canvas.delete("axes")
        self.app.draw_axes()
        self.app.canvas.delete(self._overlay_tag)

        # Rasterización de aristas
        if len(self.vertices) >= 2:
            pairs = list(zip(self.vertices, self.vertices[1:]))
            if self.closed:
                pairs.append((self.vertices[-1], self.vertices[0]))
            for (x1, y1), (x2, y2) in pairs:
                pts = self.app.draw_callback((x1, y1), (x2, y2), D.SETTINGS["active_line_algorithm"])
                for (px, py) in pts:
                    self.app._put_pixel(px, py)

        # Overlay de vértices/coords
        k = D.SETTINGS.get("pixel_size", 8)
        for (x, y) in self.vertices:
            sx = self.app.center_x + x * k
            sy = self.app.center_y - y * k
            r = max(3, k // 2)
            self.app.canvas.create_oval(
                sx - r, sy - r, sx + r, sy + r,
                fill="#ff3333", outline="",
                tags=self._overlay_tag
            )
            self.app.canvas.create_text(
                sx + 10, sy - 10,
                text=f"({x},{y})",
                fill="#000000",
                anchor="w",
                tags=self._overlay_tag
            )

        self.app._refresh_image()

    # ---------- Utilidades de matrices para la animación ----------
    @staticmethod
    def _mul(A, B):
        return [
            [
                A[0][0] * B[0][0] + A[0][1] * B[1][0] + A[0][2] * B[2][0],
                A[0][0] * B[0][1] + A[0][1] * B[1][1] + A[0][2] * B[2][1],
                A[0][0] * B[0][2] + A[0][1] * B[1][2] + A[0][2] * B[2][2],
            ],
            [
                A[1][0] * B[0][0] + A[1][1] * B[1][0] + A[1][2] * B[2][0],
                A[1][0] * B[0][1] + A[1][1] * B[1][1] + A[1][2] * B[2][1],
                A[1][0] * B[0][2] + A[1][1] * B[1][2] + A[1][2] * B[2][2],
            ],
            [
                A[2][0] * B[0][0] + A[2][1] * B[1][0] + A[2][2] * B[2][0],
                A[2][0] * B[0][1] + A[2][1] * B[1][1] + A[2][2] * B[2][1],
                A[2][0] * B[0][2] + A[2][1] * B[1][2] + A[2][2] * B[2][2],
            ],
        ]

    @staticmethod
    def _inv_affine3(M):
        a, b, c = M[0]
        d, e, f = M[1]
        det = a * e - b * d
        if det == 0:
            return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        ai, bi, di, ei = e / det, -b / det, -d / det, a / det
        ci = -(ai * c + bi * f)
        fi = -(di * c + ei * f)
        return [[ai, bi, ci], [di, ei, fi], [0, 0, 1]]

    @staticmethod
    def _dir_angle_from_ab(a, b):
        # Recta ax + by + c = 0 → vector director (-b, a)
        return math.degrees(math.atan2(a, -b)) if (a != 0 or b != 0) else 0.0

    def _seq_from_ui(self):
        params = self._collect_params()                     # mismos campos que usa "Aplicar cambios" y el GIF
        return build_matrix_sequence(params)
    
    def _reflect_targets_fx(pts):
        return [(x, -y) for (x, y) in pts]

    def _reflect_targets_fy(pts):
        return [(-x, y) for (x, y) in pts]

    def _reflect_targets_ftheta(pts, theta_deg):
        a = math.radians(theta_deg)
        nx, ny = math.sin(a), -math.cos(a)  # normal unitaria a la recta por el origen
        # normaliza por si acaso
        nlen = (nx*nx + ny*ny) ** 0.5 or 1.0
        nx, ny = nx/nlen, ny/nlen
        out = []
        for (x, y) in pts:
            d = x*nx + y*ny
            out.append((x - 2*d*nx, y - 2*d*ny))
        return out

    def _reflect_targets_fabc(pts, A, B, C):
        nlen = (A*A + B*B) ** 0.5 or 1.0
        nx, ny = A/nlen, B/nlen
        out = []
        for (x, y) in pts:
            d = (A*x + B*y + C) / nlen
            out.append((x - 2*d*nx, y - 2*d*ny))
        return out

    # ---------- Animación en canvas ----------
    def animate_and_apply(self, steps_per_op=20, per_effect_ms=1000):
        """Anima las transformaciones en el canvas y aplica el estado final."""
        if not self.vertices:
            messagebox.showwarning("Figura vacía", "Primero crea o carga una figura"); return
        seq = build_matrix_sequence(self._collect_params())
        if not seq:
            self.app.info.insert("end", "Sin transformaciones que animar.\n"); return

        frames = list(iter_frames_vertices(self.vertices, seq, steps_per_op))
        interval = max(1, per_effect_ms // steps_per_op)

        def draw_frame(i=0):
            """Dibuja el frame i-ésimo de la animación."""
            if i >= len(frames):
                # fija el estado final
                self.vertices = [(int(round(x)), int(round(y))) for (x, y) in frames[-1]] if frames else self.vertices
                self._redraw_figure()
                self.app.info.insert("end", f"Animación aplicada ({len(seq)} transformaciones).\n")
                return
            verts_f = frames[i]
            # pintar
            self.app._rebuild_framebuffer(); self.app.canvas.delete("axes"); self.app.draw_axes()
            if len(verts_f) >= 2:
                edges = list(zip(verts_f, verts_f[1:])); 
                if self.closed: edges.append((verts_f[-1], verts_f[0]))
                for (x1, y1), (x2, y2) in edges:
                    p1 = (int(round(x1)), int(round(y1))); p2 = (int(round(x2)), int(round(y2)))
                    for (px, py) in self.app.draw_callback(p1, p2, D.SETTINGS["active_line_algorithm"]):
                        self.app._put_pixel(px, py)
            k = D.SETTINGS.get("pixel_size", 8); self.app.canvas.delete(self._overlay_tag)
            for (x, y) in verts_f:
                sx = self.app.center_x + int(round(x))*k; sy = self.app.center_y - int(round(y))*k
                r = max(3, k//2)
                self.app.canvas.create_oval(sx-r, sy-r, sx+r, sy+r, fill="#ff3333", outline="", tags=self._overlay_tag)
            self.app._refresh_image()
            self.app.after(interval, lambda: draw_frame(i+1))

        draw_frame()
    # ---------- Limpieza segura ----------
    def destroy(self):
        """Limpia bindings y overlays al destruir el panel."""
        try:
            c = getattr(self.app, "canvas", None)
            if c is not None and c.winfo_exists():
                c.unbind("<Button-1>")
                try:
                    c.delete(self._overlay_tag)
                except Exception:
                    pass
        except Exception:
            pass
        super().destroy()
