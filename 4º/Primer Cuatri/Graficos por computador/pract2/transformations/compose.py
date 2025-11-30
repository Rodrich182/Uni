from .matrices import identity, matmul, T, S, R_deg, shear, reflect_x, reflect_y, reflect_through_origin_line, reflect_arbitrary_line, apply_matrix_to_points

def build_matrix_sequence(params):
    """
    params: diccionario con posibles claves en el orden deseado:
      {'tx':..., 'ty':..., 'rot':..., 'sx':..., 'sy':..., 
       'refl_x':bool, 'refl_y':bool,
       'refl_theta': ang_deg or None,
       'refl_a': a or None, 'refl_b': b or None, 'refl_c': c or None,
       'shx':..., 'shy':...}
    Devuelve lista de (nombre, M) en el orden fijo: T -> R -> S -> ReflX -> ReflY -> Refl(theta) -> Refl(a,b,c) -> Shear.
    """
    seq = []
    if params.get('tx') or params.get('ty'):
        seq.append(("T", T(params.get('tx', 0), params.get('ty', 0))))
    if params.get('rot'):
        seq.append(("R", R_deg(params.get('rot', 0))))
    if params.get('sx') not in (None, 1) or params.get('sy') not in (None, 1):
        seq.append(("S", S(params.get('sx', 1), params.get('sy', 1))))
    if params.get('refl_x'):
        seq.append(("Fx", reflect_x()))
    if params.get('refl_y'):
        seq.append(("Fy", reflect_y()))
    if params.get('refl_theta') not in (None, 0):
        seq.append(("Fθ", reflect_through_origin_line(params['refl_theta'])))
    if all(k in params for k in ('refl_a','refl_b','refl_c')) and any((params['refl_a'], params['refl_b'])):
        seq.append(("Fabc", reflect_arbitrary_line(params['refl_a'], params['refl_b'], params.get('refl_c', 0))))
    if params.get('shx') or params.get('shy'):
        seq.append(("Sh", shear(params.get('shx', 0), params.get('shy', 0))))
    return seq

def compose_all(seq):
    M = identity()
    for _name, m in seq:
        M = matmul(m, M)
    return M

def apply_all(vertices, params):
    seq = build_matrix_sequence(params)
    M = compose_all(seq)
    return apply_matrix_to_points(M, vertices), seq