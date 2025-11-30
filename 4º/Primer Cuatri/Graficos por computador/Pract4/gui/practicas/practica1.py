
import tkinter as tk
from tkinter import ttk, messagebox
import dictionary as D

class Practica1Panel(ttk.Frame):
    """
    Panel lateral de la Práctica 1.
    Reutiliza métodos y estado del objeto 'app' (LineDrawingGUI) para dibujar/limpiar/etc.
    """
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Tamaño de píxel (local de P1, pero puede leer/escribir D.SETTINGS si quieres globalizarlo)
        ttk.Label(self, text="Tamaño píxel:").grid(row=0, column=0, padx=(0,5), pady=5, sticky="e")
        self.app.pixel_size_var = tk.IntVar(value=D.SETTINGS.get("pixel_size", 8))
        ttk.Spinbox(self, from_=1, to=40, increment=1, textvariable=self.app.pixel_size_var, width=6,
                    command=self.app.on_pixel_size_change).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(self, text="Limpiar", command=self.app.clear).grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        ttk.Button(self, text="Coordenadas", command=self.app.show_coords).grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")
        ttk.Button(self, text="Lista de Puntos", command=self.app.show_points).grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

        ttk.Label(self, text="Modo Manual:").grid(row=5, column=0, padx=(0,5), pady=5, sticky="e")

        frame_coordenadas = ttk.Frame(self)
        frame_coordenadas.grid(row=6, column=0, columnspan=2, pady=5)
        ttk.Label(frame_coordenadas, text="Inicio (x1,y1):").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        self.app.entry_x1 = ttk.Entry(frame_coordenadas, width=7); self.app.entry_x1.grid(row=0, column=1, padx=2)
        ttk.Label(frame_coordenadas, text=",").grid(row=0, column=2)
        self.app.entry_y1 = ttk.Entry(frame_coordenadas, width=7); self.app.entry_y1.grid(row=0, column=3, padx=2)

        ttk.Label(frame_coordenadas, text="Fin (x2,y2):").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        self.app.entry_x2 = ttk.Entry(frame_coordenadas, width=7); self.app.entry_x2.grid(row=1, column=1, padx=2)
        ttk.Label(frame_coordenadas, text=",").grid(row=1, column=2)
        self.app.entry_y2 = ttk.Entry(frame_coordenadas, width=7); self.app.entry_y2.grid(row=1, column=3, padx=2)

        ttk.Button(self, text="Dibujar", command=self.app.dibujar_manual, width=20)\
            .grid(row=8, column=0, columnspan=2, pady=10)