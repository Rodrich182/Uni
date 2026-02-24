# animations/gif_export.py
import os
from PIL import Image, ImageDraw, ImageColor
from transformations.compose import build_matrix_sequence
from animations.runtime import iter_frames_vertices  


def _parse_color(c): 
    return ImageColor.getrgb(c)

def _to_screen(pt, canvas_size, pixel):
    #Converts a logical point to screen coordinates (0,0) top-left
    cx = canvas_size // 2; cy = canvas_size // 2
    x, y = pt
    return (cx + int(round(x * pixel)), cy - int(round(y * pixel)))

def _render_frame(vertices, closed, canvas_size, pixel_size, line_color, axis_color, bg):
    """Renders a single frame as a PIL Image.
    Draws axes, and the polygon defined by vertices (closed or not)."""
    img = Image.new("RGB", (canvas_size, canvas_size), bg)  # create blank image
    drw = ImageDraw.Draw(img)                               # create drawing context
    cx = canvas_size // 2; cy = canvas_size // 2            # center coords
    drw.line([(0, cy), (canvas_size - 1, cy)], fill=axis_color, width=1)    # X axis
    drw.line([(cx, 0), (cx, canvas_size - 1)], fill=axis_color, width=1)    # Y axis
    if len(vertices) >= 2:                                                  # draw polygon
        pairs = list(zip(vertices, vertices[1:]))                           # pairs of consecutive vertices
        if closed: pairs.append((vertices[-1], vertices[0]))
        for p1, p2 in pairs:    # draw line between p1 and p2
            drw.line([_to_screen(p1, canvas_size, pixel_size), _to_screen(p2, canvas_size, pixel_size)],
                     fill=line_color, width=max(1, pixel_size // 2))
    return img

def export_gif(vertices, closed, params, canvas_size, pixel_size, palette,
               steps_per_op=20, out_path="anim.gif", duration_ms=50):
    """Exports an animated GIF showing the transformations applied to the given vertices."""
    seq = build_matrix_sequence(params)  # mismo orden que aplicar cambios
    frames = []
    for verts in iter_frames_vertices(vertices, seq, steps_per_op): # generates frames
        frames.append(_render_frame(
            verts, closed, canvas_size, pixel_size,
            line_color=_parse_color(palette["line_color"]),
            axis_color=_parse_color(palette["axis_color"]),
            bg=_parse_color(palette["canvas_bg"])
        ))  # render frame
    if not frames:
        frames.append(_render_frame(
            vertices, closed, canvas_size, pixel_size,
            line_color=_parse_color(palette["line_color"]),
            axis_color=_parse_color(palette["axis_color"]),
            bg=_parse_color(palette["canvas_bg"])
        ))  # render at least one frame
    folder = os.path.dirname(out_path)
    if folder: os.makedirs(folder, exist_ok=True)   # ensure output folder exists
    pal = [f.convert("P", palette=Image.ADAPTIVE, colors=256) for f in frames]  # convert to paletted
    pal[0].save(out_path, save_all=True, append_images=pal[1:], optimize=True,
                duration=duration_ms, loop=0, disposal=2)   # save GIF
    return out_path
