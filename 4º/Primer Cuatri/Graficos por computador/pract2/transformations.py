# transformations.py
import math
from typing import List, Tuple, Dict

Point = Tuple[float, float]
Mat3 = List[List[float]]

def I() -> Mat3:
    return [[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]]

def matmul(A: Mat3, B: Mat3) -> Mat3:
    return [[sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

def matvec(M: Mat3, p: Point) -> Point:
    x,y = p
    xp = M[0][0]*x + M[0][1]*y + M[0][2]
    yp = M[1][0]*x + M[1][1]*y + M[1][2]
    wp = M[2][0]*x + M[2][1]*y + M[2][2]
    if wp != 0:
        xp, yp = xp/wp, yp/wp
    return (xp, yp)

def apply(M: Mat3, pts: List[Point]) -> List[Point]:
    return [matvec(M, p) for p in pts]

def compose(*Ms: Mat3) -> Mat3:
    M = I()
    for A in Ms:
        M = matmul(A, M)  # derecha a izquierda
    return M

def translate(tx: float, ty: float) -> Mat3:
    return [[1.0,0.0,tx],[0.0,1.0,ty],[0.0,0.0,1.0]]

def scale(sx: float, sy: float) -> Mat3:
    return [[sx,0.0,0.0],[0.0,sy,0.0],[0.0,0.0,1.0]]

def rotate_deg(theta_deg: float) -> Mat3:
    a = math.radians(theta_deg)
    c, s = math.cos(a), math.sin(a)
    return [[c,-s,0.0],[s,c,0.0],[0.0,0.0,1.0]]

def shear(shx: float=0.0, shy: float=0.0) -> Mat3:
    return [[1.0,shx,0.0],[shy,1.0,0.0],[0.0,0.0,1.0]]

def reflect_x() -> Mat3:
    return [[1.0,0.0,0.0],[0.0,-1.0,0.0],[0.0,0.0,1.0]]

def reflect_y() -> Mat3:
    return [[-1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]]

def reflect_through_origin_line(theta_deg: float) -> Mat3:
    # Refleja respecto a recta que pasa por el origen con ángulo theta: R(-θ)·RefX·R(θ)
    return compose(rotate_deg(-theta_deg), reflect_x(), rotate_deg(theta_deg))

def reflect_through_arbitrary_line(px: float, py: float, theta_deg: float) -> Mat3:
    # Refleja respecto a recta que pasa por (px,py) con ángulo theta
    return compose(translate(px, py),
                   rotate_deg(theta_deg),
                   reflect_x(),
                   rotate_deg(-theta_deg),
                   translate(-px, -py))
