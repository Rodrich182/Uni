# animations/gif_export.py
import os
from PIL import Image, ImageDraw, ImageColor
from transformations.compose import build_matrix_sequence
from animations.runtime import iter_frames_vertices  # NUEVO

def _parse_color(c): return ImageColor.getrgb(c)

def _to_screen(pt, canvas_size, pixel):
    cx = canvas_size // 2; cy = canvas_size // 2
    x, y = pt
    return (cx + int(round(x * pixel)), cy - int(round(y * pixel)))

def _render_frame(vertices, closed, canvas_size, pixel_size, line_color, axis_color, bg):
    img = Image.new("RGB", (canvas_size, canvas_size), bg)
    drw = ImageDraw.Draw(img)
    cx = canvas_size // 2; cy = canvas_size // 2
    drw.line([(0, cy), (canvas_size - 1, cy)], fill=axis_color, width=1)
    drw.line([(cx, 0), (cx, canvas_size - 1)], fill=axis_color, width=1)
    if len(vertices) >= 2:
        pairs = list(zip(vertices, vertices[1:]))
        if closed: pairs.append((vertices[-1], vertices[0]))
        for p1, p2 in pairs:
            drw.line([_to_screen(p1, canvas_size, pixel_size), _to_screen(p2, canvas_size, pixel_size)],
                     fill=line_color, width=max(1, pixel_size // 2))
    return img

def export_gif(vertices, closed, params, canvas_size, pixel_size, palette,
               steps_per_op=20, out_path="anim.gif", duration_ms=50):
    seq = build_matrix_sequence(params)  # mismo orden que aplicar cambios
    frames = []
    for verts in iter_frames_vertices(vertices, seq, steps_per_op):
        frames.append(_render_frame(
            verts, closed, canvas_size, pixel_size,
            line_color=_parse_color(palette["line_color"]),
            axis_color=_parse_color(palette["axis_color"]),
            bg=_parse_color(palette["canvas_bg"])
        ))
    if not frames:
        frames.append(_render_frame(
            vertices, closed, canvas_size, pixel_size,
            line_color=_parse_color(palette["line_color"]),
            axis_color=_parse_color(palette["axis_color"]),
            bg=_parse_color(palette["canvas_bg"])
        ))
    folder = os.path.dirname(out_path)
    if folder: os.makedirs(folder, exist_ok=True)
    pal = [f.convert("P", palette=Image.ADAPTIVE, colors=256) for f in frames]
    pal[0].save(out_path, save_all=True, append_images=pal[1:], optimize=True,
                duration=duration_ms, loop=0, disposal=2)
    return out_path
