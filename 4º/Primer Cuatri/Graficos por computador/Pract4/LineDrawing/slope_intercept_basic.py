def slope_intercept_basic(x1, y1, x2, y2):
    
    points = []
        

    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    for x in range(x1, x2 + 1):
        y = round(m * x + b)
        points.append((x, y))

    return points
