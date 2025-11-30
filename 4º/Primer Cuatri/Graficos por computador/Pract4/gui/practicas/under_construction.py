
from tkinter import ttk

class UnderConstructionPanel(ttk.Frame):
    def __init__(self, parent, app, label="Práctica en construcción"):
        super().__init__(parent)
        ttk.Label(self, text=label).grid(row=0, column=0, padx=10, pady=10, sticky="w")