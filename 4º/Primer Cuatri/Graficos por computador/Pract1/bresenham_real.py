def bresenham_real(x1, y1, x2, y2):
    """
    Algoritmo de Bresenham (aritmética real)
    Usa variable de error y operaciones de punto flotante.
    """
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x_step = 1 if x2 > x1 else -1
    y_step = 1 if y2 > y1 else -1
    x, y = x1, y1
    if dx > dy:
        m = dy / dx
        e = m - 0.5
        for _ in range(dx + 1):
            points.append((x, y))
            if e >= 0:
                y += y_step
                e -= 1
            x += x_step
            e += m
    else:
        m = dx / dy
        e = m - 0.5
        for _ in range(dy + 1):
            points.append((x, y))
            if e >= 0:
                x += x_step
                e -= 1
            y += y_step
            e += m
    return points
