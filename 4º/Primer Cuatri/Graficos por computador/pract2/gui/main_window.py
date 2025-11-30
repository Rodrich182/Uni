
import tkinter as tk
from tkinter import ttk, messagebox
import dictionary as D
from .theme import apply_theme

from .practicas.practica1 import Practica1Panel
from .practicas.practica2 import Practica2Panel
from .practicas.under_construction import UnderConstructionPanel

class LineDrawingGUI(ttk.Frame):
    def __init__(self, parent, draw_callback, algo_keys, default_algo,
                 canvas_size, default_pixel_size, title, win_size):
        super().__init__(parent)
        self.parent = parent
        self.draw_callback = draw_callback

        # Tema inicial
        self.palette = apply_theme(self.parent, D.SETTINGS.get("theme", "light"))

        # Ventana
        self.parent.title(title)
        self.parent.geometry(win_size)

        # Estado
        self.points = []
        self.canvas_size = canvas_size
        self.start = None
        self.end = None
        self.last_start = None
        self.last_end = None

        # Barra superior: selector de práctica
        topbar = ttk.Frame(self)
        topbar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=8, pady=(8, 4))
        for i, key in enumerate(D.PRACTICE_KEYS):
            btn = ttk.Button(topbar, text=key.capitalize(), command=lambda k=key: self.switch_practice(k))
            btn.grid(row=0, column=i, padx=4)

        # Barra global de ajustes (Algoritmo y Tema)
        settingsbar = ttk.Frame(self)
        settingsbar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=8, pady=(0, 8))

        ttk.Label(settingsbar, text="Algoritmo:").grid(row=0, column=0, padx=(0,5), sticky="e")
        self.algo_var = tk.StringVar(value=default_algo)
        algo_combo = ttk.Combobox(settingsbar, textvariable=self.algo_var, values=list(algo_keys), state="readonly", width=24)
        algo_combo.grid(row=0, column=1, padx=5, sticky="w")
        algo_combo.bind("<<ComboboxSelected>>", self._on_algo_change)

        ttk.Label(settingsbar, text="Tema:").grid(row=0, column=2, padx=(20,5), sticky="e")
        self.theme_var = tk.StringVar(value=D.SETTINGS.get("theme", "light"))
        theme_combo = ttk.Combobox(settingsbar, textvariable=self.theme_var, values=["light", "dark"], state="readonly", width=10)
        theme_combo.grid(row=0, column=3, padx=5, sticky="w")
        theme_combo.bind("<<ComboboxSelected>>", self._on_theme_change)

        # Canvas común
        self.canvas = tk.Canvas(
            self, bg=self.palette["canvas_bg"],
            width=self.canvas_size, height=self.canvas_size,
            bd=2, relief="sunken", highlightthickness=0
        )
        self.canvas.grid(row=2, column=0, padx=10, pady=10, sticky="nw")

        self.width = int(self.canvas["width"])
        self.height = int(self.canvas["height"])
        self.center_x = self.width // 2
        self.center_y = self.height // 2

        # Panel derecho contenedor (contenido específico por práctica)
        self.right_container = ttk.Frame(self)
        self.right_container.grid(row=2, column=1, padx=20, pady=10, sticky="n")
        self.current_panel = None

        # Info común
        self.info = tk.Text(self, height=10, width=100, bd=0, highlightthickness=0,
                            bg=self.palette["text_bg"], fg=self.palette["text_fg"])
        self.info.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.info.insert("end", "Selecciona práctica y dibuja con dos clics o modo manual.\n")

        # Framebuffer
        self.img = None
        self.img_zoom = None
        self.img_id = None
        self.pixel_size_var = tk.IntVar(value=D.SETTINGS.get("pixel_size", 8))
        self._rebuild_framebuffer()
        self.draw_axes()

        # Eventos
        self.canvas.bind("<Button-1>", self.on_click)
        self.grid()

        # Inicialización global
        D.SETTINGS["active_line_algorithm"] = self.algo_var.get()
        D.SETTINGS["theme"] = self.theme_var.get()

        # Carga práctica por defecto
        self.switch_practice(D.SETTINGS.get("practice", D.DEFAULT_PRACTICE))

    # Cambio de práctica: sustituye el panel derecho
    def switch_practice(self, key):
        D.SETTINGS["practice"] = key
        self.clear()
        for w in self.right_container.winfo_children():
            w.destroy()
        if key == "practica1":
            self.current_panel = Practica1Panel(self.right_container, self)
        elif key == "practica2":
            self.current_panel = Practica2Panel(self.right_container, self)
        elif key == "practica3":
            self.current_panel = UnderConstructionPanel(self.right_container, self, "Práctica 3 en construcción")
        elif key == "practica4":
            self.current_panel = UnderConstructionPanel(self.right_container, self, "Práctica 4 en construcción")
        else:
            self.current_panel = UnderConstructionPanel(self.right_container, self, "Práctica desconocida")
        self.current_panel.grid(row=0, column=0, sticky="n")

    # Ajustes globales
    def _on_algo_change(self, _evt=None):
        D.SETTINGS["active_line_algorithm"] = self.algo_var.get()

    def _on_theme_change(self, _evt=None):
        mode = self.theme_var.get()
        D.SETTINGS["theme"] = mode
        self.palette = apply_theme(self.parent, mode)
        self.canvas.configure(bg=self.palette["canvas_bg"])
        self.canvas.delete("axes")
        self.draw_axes()
        self.info.configure(bg=self.palette["text_bg"], fg=self.palette["text_fg"])
        self._refresh_image()

    # Conversión y framebuffer
    def screen_to_grid(self, sx, sy):
        k = self.pixel_size_var.get()
        gx = round(sx / k) - self.grid_w // 2
        gy = self.grid_h // 2 - round(sy / k)
        return gx, gy

    def _rebuild_framebuffer(self):
        k = self.pixel_size_var.get()
        self.grid_w = max(1, self.canvas_size // k)
        self.grid_h = max(1, self.canvas_size // k)
        self.img = tk.PhotoImage(width=self.grid_w, height=self.grid_h)
        self.img_zoom = self.img.zoom(k)
        if self.img_id is None:
            self.img_id = self.canvas.create_image(0, 0, image=self.img_zoom, anchor="nw")
        else:
            self.canvas.itemconfig(self.img_id, image=self.img_zoom)
        self.canvas.tag_lower(self.img_id)

    def _refresh_image(self):
        k = self.pixel_size_var.get()
        self.img_zoom = self.img.zoom(k)
        self.canvas.itemconfig(self.img_id, image=self.img_zoom)

    def _put_pixel(self, gx, gy, color=None):
        ix = gx + self.grid_w // 2
        iy = self.grid_h // 2 - gy
        if 0 <= ix < self.grid_w and 0 <= iy < self.grid_h:
            self.img.put(color or self.palette["line_color"], (ix, iy))

    # API de controles usada por Práctica 1
    def on_pixel_size_change(self):
        D.SETTINGS["pixel_size"] = self.pixel_size_var.get()
        self._rebuild_framebuffer()
        self.canvas.delete("axes")
        self.draw_axes()

    def clear(self):
        self.start = self.end = None
        self.last_start = self.last_end = None
        self.info.delete("1.0", "end")
        self._rebuild_framebuffer()
        self.canvas.delete("axes")
        self.draw_axes()
        self.info.insert("end", "Canvas limpio. Empieza de nuevo.\n")

    def on_click(self, event):
        gx, gy = self.screen_to_grid(event.x, event.y)
        if self.start is None:
            self.start = (gx, gy)
            self.info.insert("end", f"Inicio: {self.start}\n")
        else:
            self.end = (gx, gy)
            self.info.insert("end", f"Fin: {self.end}\n")
            algo = D.SETTINGS["active_line_algorithm"]
            self.points = self.draw_callback(self.start, self.end, algo)
            for px, py in self.points:
                self._put_pixel(px, py)
            self._refresh_image()
            self.info.insert("end", f"{algo}: {len(self.points)} puntos\n\n")
            self.last_start, self.last_end = self.start, self.end
            self.start = self.end = None

    def show_coords(self):
        if self.start is not None and self.end is None:
            msg = f"Inicio: {self.start}\nFin: None"
        elif self.last_start is not None and self.last_end is not None:
            msg = f"Inicio: {self.last_start}\nFin: {self.last_end}"
        else:
            msg = "Inicio: None\nFin: None"
        messagebox.showinfo("Coordenadas actuales", msg)

    def draw_axes(self):
        self.canvas.delete("axes")
        self.canvas.create_line(0, self.center_y, self.width, self.center_y,
                                fill=self.palette["axis_color"], width=1, tags="axes")
        self.canvas.create_line(self.center_x, 0, self.center_x, self.height,
                                fill=self.palette["axis_color"], width=1, tags="axes")
        self.canvas.tag_raise("axes")

    def show_points(self):
        if self.last_start is not None and self.last_end is not None:
            msg = "\n".join(f"{p}" for p in self.points)
        else:
            msg = "No tenemos ninguna linea guardada"
        messagebox.showinfo("Coordenadas de la última línea", msg)

    def dibujar_manual(self):
        try:
            x1 = int(self.entry_x1.get()); y1 = int(self.entry_y1.get())
            x2 = int(self.entry_x2.get()); y2 = int(self.entry_y2.get())
            self.start = (x1, y1); self.end = (x2, y2)
            algo = D.SETTINGS["active_line_algorithm"]
            self.points = self.draw_callback(self.start, self.end, algo)
            for px, py in self.points:
                self._put_pixel(px, py)
            self._refresh_image()
            self.info.insert("end", f"Manual - Inicio: {self.start}, Fin: {self.end}\n")
            self.info.insert("end", f"{algo}: {len(self.points)} puntos\n\n")
            self.last_start, self.last_end = self.start, self.end
            self.start = self.end = None
            for e in (self.entry_x1, self.entry_y1, self.entry_x2, self.entry_y2):
                e.delete(0, "end")
        except ValueError:
            messagebox.showerror("Error", "Introduce números enteros válidos")