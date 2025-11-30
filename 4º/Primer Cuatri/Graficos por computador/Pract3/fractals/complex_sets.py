# fractals/complex_sets.py

def mandelbrot_points(w, h, xmin, xmax, ymin, ymax, max_iter):
    """
    Genera una lista de (gx, gy, n) para cada celda de la rejilla w x h,
    donde n es el número de iteración en el que escapa (o max_iter si no escapa).
    gx, gy están centradas en (0,0) como en tu app.
    """
    pts = []
    for ix in range(w):
        for iy in range(h):
            x = xmin + (xmax - xmin) * ix / (w - 1)
            y = ymax - (ymax - ymin) * iy / (h - 1)

            c = complex(x, y)
            z = 0 + 0j
            n = 0
            while (z.real * z.real + z.imag * z.imag) <= 4.0 and n < max_iter:
                z = z * z + c
                n += 1

            gx = ix - w // 2
            gy = h // 2 - iy
            pts.append((gx, gy, n))
    return pts


def julia_points(w, h, xmin, xmax, ymin, ymax, c, max_iter):
    """
    Igual que mandelbrot_points, pero para conjuntos de Julia con parámetro c.
    """
    pts = []
    for ix in range(w):
        for iy in range(h):
            x = xmin + (xmax - xmin) * ix / (w - 1)
            y = ymax - (ymax - ymin) * iy / (h - 1)

            z = complex(x, y)
            n = 0
            while (z.real * z.real + z.imag * z.imag) <= 4.0 and n < max_iter:
                z = z * z + c
                n += 1

            gx = ix - w // 2
            gy = h // 2 - iy
            pts.append((gx, gy, n))
    return pts
