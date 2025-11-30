from .matrices import (
    identity, matmul, T, S, R_deg, shear,
    reflect_x, reflect_y, reflect_through_origin_line, reflect_arbitrary_line,
    apply_matrix_to_points
)
def build_matrix_sequence(params):
    seq = []
    if params.get('tx') or params.get('ty'):
        tx, ty = params.get('tx', 0), params.get('ty', 0)
        seq.append({"name":"T", "args":{"tx":tx, "ty":ty}, "M": T(tx, ty)})
    if params.get('rot'):
        rot = params.get('rot', 0)
        seq.append({"name":"R", "args":{"rot":rot}, "M": R_deg(rot)})
    sx = params.get('sx', 1); sy = params.get('sy', 1)
    if sx != 1 or sy != 1:
        seq.append({"name":"S", "args":{"sx":sx, "sy":sy}, "M": S(sx, sy)})
    if params.get('refl_x'):
        seq.append({"name":"Fx", "args":{}, "M": reflect_x()})
    if params.get('refl_y'):
        seq.append({"name":"Fy", "args":{}, "M": reflect_y()})
    if params.get('refl_theta') not in (None, 0):
        theta = params['refl_theta']
        seq.append({"name":"Fθ", "args":{"theta":theta}, "M": reflect_through_origin_line(theta)})
    if all(k in params for k in ('refl_a','refl_b','refl_c')) and any((params['refl_a'], params['refl_b'])):
        a,b,c = params['refl_a'], params['refl_b'], params.get('refl_c', 0)
        seq.append({"name":"Fabc", "args":{"a":a,"b":b,"c":c}, "M": reflect_arbitrary_line(a,b,c)})
    if params.get('shx') or params.get('shy'):
        shx, shy = params.get('shx',0), params.get('shy',0)
        seq.append({"name":"Sh", "args":{"shx":shx,"shy":shy}, "M": shear(shx, shy)})
    return seq

def compose_all(seq):
    M = identity()
    for it in seq:
        M = matmul(it["M"], M)
    return M

def apply_all(vertices, params):
    seq = build_matrix_sequence(params)
    M = compose_all(seq)
    return apply_matrix_to_points(M, vertices), seq