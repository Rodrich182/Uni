from .matrices import (
    identity, matmul, T, S, R_deg, shear,
    reflect_x, reflect_y, reflect_through_origin_line, reflect_arbitrary_line,
    apply_matrix_to_points
)
def build_matrix_sequence(params):
    """Receives a structure with many data about the transformations to apply,
    and builds a sequence of transformation matrices accordingly."""
    seq = []
    #traslation
    if params.get('tx') or params.get('ty'):
        #if tx,ty are not none/0 there is traslation
        tx, ty = params.get('tx', 0), params.get('ty', 0)
        #We create the matrix
        seq.append({"name":"T", "args":{"tx":tx, "ty":ty}, "M": T(tx, ty)})
    
    #Rotation
    if params.get('rot'):
        rot = params.get('rot', 0)
        seq.append({"name":"R", "args":{"rot":rot}, "M": R_deg(rot)})

    #S Scaling
    sx = params.get('sx', 1); sy = params.get('sy', 1)
    if sx != 1 or sy != 1:
        seq.append({"name":"S", "args":{"sx":sx, "sy":sy}, "M": S(sx, sy)})
    
    #X/Y Reflections
    if params.get('refl_x'):
        seq.append({"name":"Fx", "args":{}, "M": reflect_x()})
    if params.get('refl_y'):
        seq.append({"name":"Fy", "args":{}, "M": reflect_y()})

    #reflection through arbitrary lines
    if params.get('refl_theta') not in (None, 0):
        theta = params['refl_theta']
        seq.append({"name":"Fθ", "args":{"theta":theta}, "M": reflect_through_origin_line(theta)})
    
    #Arbitrary line reflection with ax+by+c=0
    if all(k in params for k in ('refl_a','refl_b','refl_c')) and any((params['refl_a'], params['refl_b'])):
        a,b,c = params['refl_a'], params['refl_b'], params.get('refl_c', 0)
        seq.append({"name":"Fabc", "args":{"a":a,"b":b,"c":c}, "M": reflect_arbitrary_line(a,b,c)})
    
    #Shearing
    if params.get('shx') or params.get('shy'):
        shx, shy = params.get('shx',0), params.get('shy',0)
        seq.append({"name":"Sh", "args":{"shx":shx,"shy":shy}, "M": shear(shx, shy)})
    
    return seq

def compose_all(seq):
    """This uses that step list and composes all the matrices into one."""
    M = identity()         
    for it in seq:
        M = matmul(it["M"], M)
    return M

def apply_all(vertices, params):
    """Applies all the transformations specified in params to the given vertices."""
    seq = build_matrix_sequence(params)
    M = compose_all(seq)
    return apply_matrix_to_points(M, vertices), seq