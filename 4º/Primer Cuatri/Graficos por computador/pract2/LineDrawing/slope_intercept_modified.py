def slope_intercept_modified(x1, y1, x2, y2):
    """
    Algoritmo Slope Intercept modificado
    Maneja todos los cuadrantes y pendientes |m|>1 intercambiando ejes.
    """
    points = []
    # Asegurar x1 ≤ x2
    if x2 < x1:
        x1, y1, x2, y2 = x2, y2, x1, y1

    dx = x2 - x1
    dy = y2 - y1
    if dx == 0:
        # Vertical
        for y in range(min(y1,y2), max(y1,y2)+1):
            points.append((x1, y))
    elif dy == 0:
        # Horizontal
        for x in range(x1, x2+1):
            points.append((x, y1))
    else:
        m = dy / dx
        if abs(m) > 1:
            # Intercambiar roles
            m_inv = dx / dy
            b = x1 - m_inv * y1
            for y in range(min(y1,y2), max(y1,y2)+1):
                x = round(m_inv * y + b)
                points.append((x, y))
        else:
            b = y1 - m * x1
            for x in range(x1, x2+1):
                y = round(m * x + b)
                points.append((x, y))
    return points
