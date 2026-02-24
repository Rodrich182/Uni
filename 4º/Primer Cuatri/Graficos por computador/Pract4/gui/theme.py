
from tkinter import ttk

def apply_theme(root, mode="light"):
    """
    Aplica un tema claro u oscuro a la aplicación Tkinter."""
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except:
        pass

    if mode == "dark":
        bg = "#181a1b"
        fg = "#e6e6e6"
        fg_muted = "#b0b0b0"
        entry_bg = "#1f2123"
        border = "#2a2c2e"
        highlight = "#3a3d40"
        canvas_bg = "#111315"
        axis_color = "#5a5a5a"
        line_color = "#66aaff"
    else:
        bg = "#f7f7f7"
        fg = "#1a1a1a"
        fg_muted = "#404040"
        entry_bg = "white"
        border = "#d9d9d9"
        highlight = "#e6e6e6"
        canvas_bg = "white"
        axis_color = "#a0a0a0"
        line_color = "#0066ff"

    root.configure(bg=bg)
    style.configure(".", background=bg, foreground=fg, font=("Segoe UI", 10))
    style.configure("TFrame", background=bg)
    style.configure("TLabelframe", background=bg)
    style.configure("TLabelframe.Label", background=bg, foreground=fg)
    style.configure("TLabel", background=bg, foreground=fg)
    style.configure("TButton", padding=(6, 6))
    style.map("TButton", background=[("active", highlight)])
    style.configure("TCombobox", fieldbackground=entry_bg, background=entry_bg, foreground=fg)
    style.configure("TEntry", fieldbackground=entry_bg, foreground=fg)
    style.configure("TSpinbox", fieldbackground=entry_bg, foreground=fg)

    return {
        "canvas_bg": canvas_bg,
        "axis_color": axis_color,
        "line_color": line_color,
        "text_fg": fg,
        "text_bg": bg,
    }