def slope_intercept_basic(x1, y1, x2, y2):
    """
    Algoritmo Slope Intercept básico
    Usa y = m·x + b con aritmética de punto flotante.
    """
    points = []
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0:
        # Línea vertical
        y_start, y_end = sorted((y1, y2))
        for y in range(y_start, y_end + 1):
            points.append((x1, y))
    else:
        m = dy / dx
        b = y1 - m * x1
        if abs(m) <= 1:
            # Incremento en x
            x_start, x_end = sorted((x1, x2))
            for x in range(x_start, x_end + 1):
                y = round(m * x + b)
                points.append((x, y))
        else:
            # Incremento en y
            y_start, y_end = sorted((y1, y2))
            for y in range(y_start, y_end + 1):
                x = round((y - b) / m)
                points.append((x, y))
    return points
