def bresenham_integer(x1, y1, x2, y2):
    """
    Algoritmo de Bresenham (aritmética entera)
    Versión optimizada usando solo operaciones con enteros.
    """
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x_step = 1 if x2 > x1 else -1
    y_step = 1 if y2 > y1 else -1
    x, y = x1, y1
    if dx > dy:
        e = 2*dy - dx
        for _ in range(dx + 1):
            points.append((x, y))
            if e >= 0:
                y += y_step
                e -= 2*dx
            x += x_step
            e += 2*dy
    else:
        e = 2*dx - dy
        for _ in range(dy + 1):
            points.append((x, y))
            if e >= 0:
                x += x_step
                e -= 2*dy
            y += y_step
            e += 2*dx
    return points
