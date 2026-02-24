# animations/runtime.py
import math
from transformations.matrices import T as Tm, R_deg as Rm, S as Sm, shear as ShearM

def mat_mul(A,B):
     return [[sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

def mat_inv_affine(M):
    """Inverts a 3x3 affine transformation matrix."""
    a,b,c = M[0]; d,e,f = M[1]; det = a*e - b*d # determinant
    if det == 0: 
        return [[1,0,0],[0,1,0],[0,0,1]]
    
    ai, bi, di, ei = e/det, -b/det, -d/det, a/det   # inverse of upper-left 2x2
    ci = -(ai*c + bi*f); fi = -(di*c + ei*f)        # inverse translation
    return [[ai,bi,ci],[di,ei,fi],[0,0,1]]          # return inverse matrix

def apply_float(M, pts):
    """Applies a 3x3 transformation matrix to a list of (x,y) points, using float arithmetic."""
    out = []
    for (x,y) in pts:
        x2 = M[0][0]*x + M[0][1]*y + M[0][2]    
        y2 = M[1][0]*x + M[1][1]*y + M[1][2]
        w  = M[2][0]*x + M[2][1]*y + M[2][2]
        if w: x2/=w; y2/=w  
        out.append((x2,y2))
    return out

def reflect_targets_fx(pts):  
    """Reflects points through the X axis."""   
    return [(x,-y) for (x,y) in pts]

def reflect_targets_fy(pts):   
    """Reflects points through the Y axis."""  
    return [(-x,y) for (x,y) in pts]

def reflect_targets_ftheta(pts, theta_deg):
    """Reflects points through the line passing through the origin at angle theta."""
    a = math.radians(theta_deg); nx, ny = math.sin(a), -math.cos(a)
    nlen = (nx*nx + ny*ny)**0.5 or 1.0; nx, ny = nx/nlen, ny/nlen
    out=[]
    for (x,y) in pts:
        d = x*nx + y*ny; out.append((x-2*d*nx, y-2*d*ny))
    return out

def reflect_targets_fabc(pts, A,B,C):
    """Reflects points through the line Ax + By + C = 0."""
    nlen = (A*A + B*B)**0.5 or 1.0; nx, ny = A/nlen, B/nlen
    out=[]
    for (x,y) in pts:
        d = (A*x + B*y + C)/nlen; out.append((x-2*d*nx, y-2*d*ny))
    return out

def abs_list(it, n):
    """Generates a list of n absolute transformation matrices for the given step."""
    name, a = it["name"], it["args"]
    if name == "T":
        tx,ty=a["tx"],a["ty"];   return [Tm(tx*t/n, ty*t/n) for t in range(1,n+1)]
    if name == "R":
        ang=a["rot"];            return [Rm(ang*t/n) for t in range(1,n+1)]
    if name == "S":
        sx,sy=a["sx"],a["sy"];   return [Sm(1+(sx-1)*t/n, 1+(sy-1)*t/n) for t in range(1,n+1)]
    if name == "Sh":
        shx,shy=a["shx"],a["shy"]; return [ShearM(shx*t/n, shy*t/n) for t in range(1,n+1)]
    return []

def iter_frames_vertices(vertices, seq, steps_per_op):
    """Generates frames of transformed vertices according to the sequence of transformations.
    For reflections, generates direct interpolation between original and target positions."""
    cur = [(float(x), float(y)) for (x,y) in vertices]  # current vertex positions
    for it in seq:
        name, a = it["name"], it["args"]
        if name in ("Fx","Fy","Fθ","Fabc"):
            orig = list(cur)
            if name == "Fx":
                tgt = reflect_targets_fx(orig)
            elif name == "Fy":
                tgt = reflect_targets_fy(orig)
            elif name == "Fθ":
                tgt = reflect_targets_ftheta(orig, a["theta"])
            else:
                tgt = reflect_targets_fabc(orig, a["a"], a["b"], a["c"])
            for t in range(1, steps_per_op+1):
                u = t/steps_per_op
                cur = [(ox + u*(tx-ox), oy + u*(ty-oy)) for (ox,oy),(tx,ty) in zip(orig, tgt)]
                yield cur
        else:
            Mprev = [[1,0,0],[0,1,0],[0,0,1]]
            for Mabs in abs_list(it, steps_per_op):
                Mdelta = mat_mul(Mabs, mat_inv_affine(Mprev))
                Mprev = Mabs
                cur = apply_float(Mdelta, cur)
                yield cur
