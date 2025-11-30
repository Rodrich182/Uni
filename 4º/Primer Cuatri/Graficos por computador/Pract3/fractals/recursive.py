# fractals/recursive.py
import math


def sierpinski_segments(level: int, size: int):
    """
    Devuelve una lista de segmentos (x1, y1, x2, y2) que forman
    un triángulo de Sierpinski centrado en el origen.
    """
    p1 = (-size, -size)   # izquierda-abajo
    p2 = (size, -size)    # derecha-abajo
    p3 = (0, size)        # arriba

    segments = []

    def rec(a, b, c, n):
        if n == 0:
            segments.extend([
                (a[0], a[1], b[0], b[1]),
                (b[0], b[1], c[0], c[1]),
                (c[0], c[1], a[0], a[1]),
            ])
        else:
            ab = ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)
            bc = ((b[0] + c[0]) // 2, (b[1] + c[1]) // 2)
            ca = ((c[0] + a[0]) // 2, (c[1] + a[1]) // 2)
            rec(a, ab, ca, n - 1)
            rec(ab, b, bc, n - 1)
            rec(ca, bc, c, n - 1)

    rec(p1, p2, p3, level)
    return segments


def koch_segments(level: int, length: int):
    """
    Devuelve una lista de segmentos (x1, y1, x2, y2) de la curva de Koch
    sobre un segmento horizontal centrado en el origen.
    """
    x1, y1 = -length // 2, 0
    x2, y2 = length // 2, 0

    segments = []

    def rec(a, b, n):
        if n == 0:
            segments.append((a[0], a[1], b[0], b[1]))
        else:
            ax, ay = a
            bx, by = b

            sx = (2 * ax + bx) / 3.0
            sy = (2 * ay + by) / 3.0
            tx = (ax + 2 * bx) / 3.0
            ty = (ay + 2 * by) / 3.0

            vx = tx - sx
            vy = ty - sy
            angle = math.radians(60.0)
            ux = sx + vx * math.cos(angle) - vy * math.sin(angle)
            uy = sy + vx * math.sin(angle) + vy * math.cos(angle)

            p1 = (ax, ay)
            p2 = (sx, sy)
            p3 = (ux, uy)
            p4 = (tx, ty)
            p5 = (bx, by)

            rec(p1, p2, n - 1)
            rec(p2, p3, n - 1)
            rec(p3, p4, n - 1)
            rec(p4, p5, n - 1)

    rec((x1, y1), (x2, y2), level)
    return segments
