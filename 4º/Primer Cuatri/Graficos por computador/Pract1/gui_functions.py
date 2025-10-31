"""
Funciones auxiliares para la interfaz gráfica
"""

def screen_to_grid(sx, sy, canvas_size, grid_w, grid_h, pixel_size):
    """
    Convierte coordenadas de pantalla a coordenadas de cuadrícula lógica
    
    Args:
        sx, sy: coordenadas de pantalla
        canvas_size: tamaño del canvas
        grid_w, grid_h: dimensiones de la cuadrícula
        pixel_size: factor de escala (k)
    
    Returns:
        tupla (gx, gy) en coordenadas de cuadrícula
    """
    gx = round(sx / pixel_size) - grid_w // 2
    gy = grid_h // 2 - round(sy / pixel_size)
    return gx, gy


def grid_to_screen(gx, gy, center_x, center_y, pixel_size):
    """
    Convierte coordenadas de cuadrícula a coordenadas de pantalla
    
    Args:
        gx, gy: coordenadas de cuadrícula
        center_x, center_y: centro del canvas en pantalla
        pixel_size: factor de escala (k)
    
    Returns:
        tupla (sx, sy) en coordenadas de pantalla
    """
    sx = center_x + gx * pixel_size
    sy = center_y - gy * pixel_size
    return sx, sy


def put_pixel(img, gx, gy, grid_w, grid_h, color="#0000ff"):
    """
    Dibuja un píxel en el framebuffer lógico
    
    Args:
        img: PhotoImage donde dibujar
        gx, gy: coordenadas de cuadrícula
        grid_w, grid_h: dimensiones de la cuadrícula
        color: color del píxel en formato hexadecimal
    """
    ix = gx + grid_w // 2
    iy = grid_h // 2 - gy
    if 0 <= ix < grid_w and 0 <= iy < grid_h:
        img.put(color, (ix, iy))


def format_points_message(points):
    """
    Formatea la lista de puntos para mostrar en messagebox
    
    Args:
        points: lista de tuplas (x, y)
    
    Returns:
        string formateado con los puntos
    """
    if len(points) > 100:
        # Si hay muchos puntos, mostrar solo los primeros 100
        msg = "\n".join(str(p) for p in points[:100])
        msg += f"\n\n... y {len(points) - 100} píxeles más"
    else:
        msg = "\n".join(str(p) for p in points)
    return msg


def format_coords_message(start, end, last_start, last_end):
    """
    Formatea el mensaje de coordenadas actuales
    
    Args:
        start: punto inicial actual (o None)
        end: punto final actual (o None)
        last_start: último punto inicial guardado
        last_end: último punto final guardado
    
    Returns:
        string formateado con las coordenadas
    """
    if start is not None and end is None:
        return f"Inicio: {start}\nFin: None"
    elif last_start is not None and last_end is not None:
        return f"Inicio: {last_start}\nFin: {last_end}"
    else:
        return "Inicio: None\nFin: None"
