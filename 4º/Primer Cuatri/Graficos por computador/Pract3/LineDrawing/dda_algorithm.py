def dda_algorithm(x1, y1, x2, y2):
    """
    Algoritmo DDA (Digital Differential Analyzer)
    Usa incrementos constantes en x e y.
    """
    points = []
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return [(x1, y1)]
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1 + 0.5, y1 + 0.5
    for _ in range(steps + 1):
        points.append((int(x), int(y)))
        x += x_inc
        y += y_inc
    return points