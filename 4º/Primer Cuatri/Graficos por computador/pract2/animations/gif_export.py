
from PIL import Image, ImageDraw, ImageFont
import math
from transformations.compose import build_matrix_sequence
from transformations.matrices import identity, matmul, apply_matrix_to_points, T, R_deg, S, shear

def _canvas_to_image_coords(x, y, canvas_size, pixel_size):
    # Grid centrado: origen en el centro del canvas, y hacia arriba
    # Convertimos (x,y) de grid a píxel de imagen
    cx = canvas_size // 2 + x * pixel_size
    cy = canvas_size // 2 - y * pixel_size
    return cx, cy

def _draw_axes(draw, canvas_size, axis_color=(128,128,128)):
    mid = canvas_size // 2
    draw.line([(0, mid), (canvas_size, mid)], fill=axis_color, width=1)
    draw.line([(mid, 0), (mid, canvas_size)], fill=axis_color, width=1)

def _render_frame(vertices, closed, canvas_size, pixel_size, line_color=(0,102,255), axis_color=(128,128,128), bg=(255,255,255)):
    img = Image.new("RGB", (canvas_size, canvas_size), color=bg)
    draw = ImageDraw.Draw(img)
    _draw_axes(draw, canvas_size, axis_color=axis_color)
    # Dibujar aristas
    if len(vertices) >= 2:
        pairs = list(zip(vertices, vertices[1:]))
        if closed:
            pairs.append((vertices[-1], vertices[0]))
        for (x1,y1),(x2,y2) in pairs:
            p1 = _canvas_to_image_coords(x1, y1, canvas_size, pixel_size)
            p2 = _canvas_to_image_coords(x2, y2, canvas_size, pixel_size)
            draw.line([p1, p2], fill=line_color, width=max(1, pixel_size//2))
    # Dibujar vértices
    for (x,y) in vertices:
        sx, sy = _canvas_to_image_coords(x, y, canvas_size, pixel_size)
        r = max(2, pixel_size//2)
        draw.ellipse((sx-r, sy-r, sx+r, sy+r), fill=line_color)
        draw.text((sx + 6, sy - 10), f"({x},{y})", fill=line_color)
    return img

def _interp_seq_ops(seq, steps_per_op):
    # Genera secuencia de matrices incrementales para animar cada op de forma secuencial
    for name, M_full in seq:
        for i in range(1, steps_per_op+1):
            t = i/steps_per_op
            # Aproximación: derivar parámetros básicos para interpolar
            if name == "T":
                tx, ty = M_full[0][2], M_full[1][2]
                yield name, T(t*tx, t*ty)
            elif name == "R":
                # extraer ángulo de M_full
                import math
                angle = math.degrees(math.atan2(M_full[1][0], M_full[0][0]))
                yield name, R_deg(t*angle)
            elif name == "S":
                sx, sy = M_full[0][0], M_full[1][1]
                sx_t = 1 + t*(sx-1)
                sy_t = 1 + t*(sy-1)
                yield name, S(sx_t, sy_t)
            elif name in ("Fx","Fy","Fθ","Fabc"):
                # Aproximar como una escala continua pasando por -1 en el eje principal
                # Para Fx: S(1, s(t)) con s: 1→-1, para Fy: S(s(t),1)
                if name == "Fx":
                    s = 1 - 2*t
                    yield name, S(1, s)
                elif name == "Fy":
                    s = 1 - 2*t
                    yield name, S(s, 1)
                else:
                    # Fθ y Fabc ya vienen compuestas, se anima con raíz matricial aproximada por interpolación de ángulo y escala
                    yield name, _matrix_power_approx(M_full, t)
            elif name == "Sh":
                shx, shy = M_full[0][1], M_full[1][0]
                yield name, shear(t*shx, t*shy)

def _matrix_power_approx(M, t):
    # Aproximación simple: combinación convexa con identidad en espacio de parámetros
    # No es una raíz exacta general, pero produce una transición suave visualmente
    # Descomponer M ≈ R S Sh T ignorando T en animación incremental
    # Aquí devolvemos una mezcla diagonal + rotación extraída
    import math
    angle = math.degrees(math.atan2(M[1][0], M[0][0]))
    c, s = math.cos(math.radians(angle*t)), math.sin(math.radians(angle*t))
    R = [[c,-s,0],[s,c,0],[0,0,1]]
    sx = M[0][0] if M[0][0] != 0 else 1
    sy = M[1][1] if M[1][1] != 0 else 1
    sx_t = 1 + t*(sx-1)
    sy_t = 1 + t*(sy-1)
    S_t = [[sx_t,0,0],[0,sy_t,0],[0,0,1]]
    # R * S_t
    return [[R[0][0]*S_t[0][0], R[0][1]*S_t[1][1], 0],
            [R[1][0]*S_t[0][0], R[1][1]*S_t[1][1], 0],
            [0,0,1]]

def export_gif(vertices, closed, params, canvas_size, pixel_size, palette, steps_per_op=20, out_path="anim.gif", duration_ms=30):
    seq = build_matrix_sequence(params)
    frames = []
    cur_vertices = list(vertices)
    for name, M_i in _interp_seq_ops(seq, steps_per_op):
        cur_vertices = apply_matrix_to_points(M_i, cur_vertices)
        img = _render_frame(
            cur_vertices, closed, canvas_size, pixel_size,
            line_color=_hex_to_rgb(palette["line_color"]),
            axis_color=_hex_to_rgb(palette["axis_color"]),
            bg=_hex_to_rgb(palette["canvas_bg"])
        )
        frames.append(img)
    if not frames:
        # Generar un fotograma estático si no hay transformaciones
        frames.append(_render_frame(vertices, closed, canvas_size, pixel_size,
                                    line_color=_hex_to_rgb(palette["line_color"]),
                                    axis_color=_hex_to_rgb(palette["axis_color"]),
                                    bg=_hex_to_rgb(palette["canvas_bg"])))
    frames[0].save(out_path, save_all=True, append_images=frames[1:], optimize=True, duration=duration_ms, loop=0)
    return out_path

def _hex_to_rgb(hx):
    hx = hx.lstrip("#")
    return tuple(int(hx[i:i+2], 16) for i in (0,2,4))