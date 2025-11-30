# gui/practicas/practica4.py

import tkinter as tk
from tkinter import ttk, messagebox

import dictionary as D
from lsystems import apply_rules, turtle_segments, PRESETS


class Practica4Panel(ttk.Frame):
    """
    Práctica 4: L-sistemas
    - Selección de ejemplo (Koch, Sierpinski, Dragón, Planta)
    - Ajuste de iteraciones, ángulo y longitud
    - Generación de cadena por reglas de L-sistema
    - Interpretación gráfica con tortuga y rasterización mediante algoritmos de línea
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # ---------- Estado ----------
        self.system_key = tk.StringVar(value=D.DEFAULT_L_SYSTEM)
        self.iter_var = tk.IntVar(value=D.DEFAULT_LSYS_ITER)
        self.angle_var = tk.DoubleVar(value=D.DEFAULT_LSYS_ANGLE)
        self.length_var = tk.DoubleVar(value=D.DEFAULT_LSYS_LENGTH)

        self.animate_var = tk.BooleanVar(value=False)
        self.max_iter_limit = D.MAX_LSYS_ITER

        # Construir UI
        self._build_ui()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _build_ui(self):
        config_frame = ttk.LabelFrame(self, text="Configuración L-sistema")
        config_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Tipo de sistema
        ttk.Label(config_frame, text="Ejemplo:").grid(row=0, column=0, sticky="e")
        system_combo = ttk.Combobox(
            config_frame,
            textvariable=self.system_key,
            values=D.L_SYSTEM_KEYS,
            state="readonly",
            width=15,
        )
        system_combo.grid(row=0, column=1, sticky="w", padx=4)
        system_combo.bind("<<ComboboxSelected>>", self._on_system_change)

        # Iteraciones
        ttk.Label(config_frame, text="Iteraciones:").grid(
            row=0, column=2, sticky="e", padx=6
        )
        iter_spin = tk.Spinbox(
            config_frame,
            from_=0,
            to=self.max_iter_limit,
            textvariable=self.iter_var,
            width=5,
        )
        iter_spin.grid(row=0, column=3, sticky="w")

        # Ángulo
        ttk.Label(config_frame, text="Ángulo (°):").grid(
            row=1, column=0, sticky="e", pady=(4, 0)
        )
        angle_entry = ttk.Entry(config_frame, textvariable=self.angle_var, width=8)
        angle_entry.grid(row=1, column=1, sticky="w", padx=4, pady=(4, 0))

        # Longitud
        ttk.Label(config_frame, text="Longitud inicial:").grid(
            row=1, column=2, sticky="e", pady=(4, 0)
        )
        length_entry = ttk.Entry(config_frame, textvariable=self.length_var, width=8)
        length_entry.grid(row=1, column=3, sticky="w", padx=4, pady=(4, 0))

        # Botones
        btn_frame = ttk.Frame(config_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=8, sticky="ew")

        ttk.Checkbutton(
            btn_frame,
            text="Animar crecimiento (0..n)",
            variable=self.animate_var,
        ).grid(row=0, column=0, padx=4, sticky="w")

        ttk.Button(
            btn_frame,
            text="Generar / Dibujar",
            command=self.on_draw,
        ).grid(row=0, column=1, padx=8, sticky="e")

        # Se expande
        self.grid_columnconfigure(0, weight=1)

        # Info inicial
        self._update_info_for_current_system()

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------

    def _prepare_canvas(self, msg: str):
        """Limpia el canvas y escribe mensaje en el área de info común."""
        self.app.clear()
        try:
            self.app.info.insert("end", msg + "\n")
        except Exception:
            pass

    def _current_preset(self):
        key = self.system_key.get()
        return PRESETS.get(key)

    def _update_info_for_current_system(self):
        preset = self._current_preset()
        if not preset:
            return
        text = (
            f"L-sistema seleccionado: {preset.name}\n"
            f"Descripción: {preset.description}\n"
            f"Fenómeno/modelo: {preset.natural_phenomenon}\n"
        )
        try:
            self.app.info.insert("end", text + "\n")
        except Exception:
            pass

    def _on_system_change(self, _evt=None):
        """Al cambiar de sistema, actualiza ángulo/longitud por defecto e info."""
        preset = self._current_preset()
        if not preset:
            return
        self.angle_var.set(preset.default_angle)
        self.length_var.set(preset.default_length)
        self._update_info_for_current_system()

    # ------------------------------------------------------------------
    # Lógica principal de dibujo
    # ------------------------------------------------------------------

    def on_draw(self):
        preset = self._current_preset()
        if not preset:
            messagebox.showerror("Error", "L-sistema desconocido.")
            return

        try:
            n_iter = int(self.iter_var.get())
        except Exception:
            messagebox.showerror("Error", "Iteraciones debe ser un entero.")
            return

        if n_iter < 0 or n_iter > self.max_iter_limit:
            messagebox.showerror(
                "Error",
                f"Las iteraciones deben estar entre 0 y {self.max_iter_limit}.",
            )
            return

        angle = float(self.angle_var.get())
        length = float(self.length_var.get())

        if length <= 0:
            messagebox.showerror("Error", "La longitud debe ser > 0.")
            return

        # Animado o solo un estado
        if self.animate_var.get() and n_iter > 0:
            self._animate_growth(preset, n_iter, angle, length)
        else:
            self._draw_state(preset, n_iter, angle, length)

    def _draw_state(self, preset, n_iter: int, angle: float, length: float):
        """Genera la cadena para n_iter y la dibuja en el canvas."""
        self._prepare_canvas(
            f"Dibujando L-sistema '{preset.name}' con {n_iter} iteraciones..."
        )

        seq = apply_rules(preset.axiom, preset.rules, n_iter)
        segs = turtle_segments(seq, angle_deg=angle, step=length)

        algo = D.SETTINGS["active_line_algorithm"]

        for x1, y1, x2, y2 in segs:
            # Ajuste opcional de escala para que quepa mejor en el lienzo
            # Escalamos usando el grid_w/grid_h
            # (factor sencillo: 0.5 para no salirnos)
            scale = 0.5
            sx1 = int(round(x1 * scale))
            sy1 = int(round(y1 * scale))
            sx2 = int(round(x2 * scale))
            sy2 = int(round(y2 * scale))

            pts = self.app.draw_callback((sx1, sy1), (sx2, sy2), algo)
            for px, py in pts:
                self.app._put_pixel(px, py)

        self.app._refresh_image()

    def _animate_growth(self, preset, max_iter: int, angle: float, length: float):
        """Animación simple: dibuja iteraciones 0..max_iter con un pequeño retardo."""
        delay_ms = 700  # se puede hacer configurable

        def step_draw(k: int):
            if k > max_iter:
                return
            self._draw_state(preset, k, angle, length)
            self.app.after(delay_ms, lambda: step_draw(k + 1))

        step_draw(0)
