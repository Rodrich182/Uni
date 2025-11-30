# fractals/ifs.py
import random


def barnsley_points(w, h, iters, skip):
    """
    Devuelve puntos (gx, gy) del helecho de Barnsley en la rejilla w x h.
    """
    pts = []

    scale = min(w, h) / 12.0
    y_offset = -h * 0.25 / (scale or 1.0)

    x, y = 0.0, 0.0
    for i in range(iters):
        r = random.random()
        if r < 0.01:
            x_new = 0.0
            y_new = 0.16 * y
        elif r < 0.86:
            x_new = 0.85 * x + 0.04 * y
            y_new = -0.04 * x + 0.85 * y + 1.6
        elif r < 0.93:
            x_new = 0.20 * x - 0.26 * y
            y_new = 0.23 * x + 0.22 * y + 1.6
        else:
            x_new = -0.15 * x + 0.28 * y
            y_new = 0.26 * x + 0.24 * y + 0.44
        x, y = x_new, y_new

        if i < skip:
            continue

        gx = int(x * scale)
        gy = int((y + y_offset) * scale)
        pts.append((gx, gy))
    return pts


def sierpinski_ifs_points(w, h, iters, skip):
    """
    Devuelve puntos (gx, gy) del triángulo de Sierpinski por IFS.
    """
    pts = []

    size = min(w, h) / 2.5
    p1 = (-size, -size)
    p2 = (size, -size)
    p3 = (0.0, size)

    transforms = [
        (0.5, 0.0, 0.0, 0.5, p1[0] / 2.0, p1[1] / 2.0),
        (0.5, 0.0, 0.0, 0.5, p2[0] / 2.0, p2[1] / 2.0),
        (0.5, 0.0, 0.0, 0.5, p3[0] / 2.0, p3[1] / 2.0),
    ]

    x, y = 0.0, 0.0
    for i in range(iters):
        a, b, c, d, e, f = random.choice(transforms)
        x, y = a * x + b * y + e, c * x + d * y + f

        if i < skip:
            continue

        gx = int(x)
        gy = int(y)
        pts.append((gx, gy))
    return pts
