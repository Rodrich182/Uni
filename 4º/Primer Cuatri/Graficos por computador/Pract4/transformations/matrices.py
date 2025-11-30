# transformations/matrices.py

import math

def T(tx, ty):
    return [[1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]]

def S(sx, sy):
    return [[sx, 0,  0],
            [0,  sy, 0],
            [0,  0,  1]]

def R_deg(theta_deg):
    a = math.radians(theta_deg)
    c, s = math.cos(a), math.sin(a)
    return [[c, -s, 0],
            [s,  c, 0],
            [0,  0, 1]]

def shear(shx=0.0, shy=0.0):
    return [[1,  shx, 0],
            [shy, 1,  0],
            [0,  0,  1]]

def reflect_x():
    return [[1, 0, 0],
            [0,-1, 0],
            [0, 0, 1]]

def reflect_y():
    return [[-1,0, 0],
            [0, 1, 0],
            [0, 0, 1]]

def reflect_through_origin_line(theta_deg):
    # Reflexión respecto de recta que pasa por el origen con ángulo theta
    # M = R(-θ) · Sx(-1) · R(θ)
    return matmul(matmul(R_deg(-theta_deg), S(-1, 1)), R_deg(theta_deg))

def reflect_arbitrary_line(a, b, c):
    # Recta: a x + b y + c = 0
    # Traslada la recta al origen, aplica Householder respecto de (a,b), y deshace la traslación
    # Traslación necesaria: d = c/(a^2+b^2) en dirección normal (a,b)
    denom = a*a + b*b
    if denom == 0:
        return identity()
    tx = -a * c / denom
    ty = -b * c / denom
    H = householder(a, b)  # reflexión respecto a línea a x + b y = 0 (por el origen)
    return matmul(matmul(T(-tx, -ty), H), T(tx, ty))

def householder(a, b):
    # Householder: Q = I - 2 n n^T, con n normalizado al vector normal (a,b)
    import math
    norm = math.hypot(a, b)
    if norm == 0:
        return identity()
    nx, ny = a/norm, b/norm
    # Matriz 2x2: I - 2 n n^T
    q11 = 1 - 2*nx*nx
    q12 = -2*nx*ny
    q21 = -2*ny*nx
    q22 = 1 - 2*ny*ny
    return [[q11, q12, 0],
            [q21, q22, 0],
            [0,   0,   1]]

def identity():
    return [[1,0,0],[0,1,0],[0,0,1]]

def matmul(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

def apply_matrix_to_points(M, vertices):
    out = []
    for (x, y) in vertices:
        X = M[0][0]*x + M[0][1]*y + M[0][2]*1
        Y = M[1][0]*x + M[1][1]*y + M[1][2]*1
        W = M[2][0]*x + M[2][1]*y + M[2][2]*1
        if W != 0:
            X, Y = X/W, Y/W
        out.append((round(X), round(Y)))
    return out
