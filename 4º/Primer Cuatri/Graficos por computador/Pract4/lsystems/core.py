# lsystems/core.py
import math


def apply_rules(axiom: str, rules: dict[str, str], iterations: int) -> str:
    """
    Aplica las reglas de un L-sistema 'iterations' veces sobre el axioma.
    Reescritura paralela: cada símbolo se sustituye en cada paso.
    """
    current = axiom
    for _ in range(iterations):
        next_str = []
        for ch in current:
            next_str.append(rules.get(ch, ch))  # si no hay regla, deja el símbolo
        current = "".join(next_str)
    return current


def turtle_segments(
    sequence: str,
    angle_deg: float,
    step: float,
    initial_angle_deg: float = 90.0,
    draw_symbols: set[str] | None = None,
    move_symbols: set[str] | None = None,
) -> list[tuple[float, float, float, float]]:
    """
    Interpreta la cadena con un intérprete de tortuga 2D y devuelve
    segmentos (x1, y1, x2, y2) en coordenadas lógicas (origen en el centro).
    Usa [, ] para manejar una pila de estados (ramas).
    """
    if draw_symbols is None:
        draw_symbols = {"F", "G"}
    if move_symbols is None:
        move_symbols = {"f"}

    x, y = 0.0, 0.0
    heading = math.radians(initial_angle_deg)
    stack: list[tuple[float, float, float]] = []
    segs: list[tuple[float, float, float, float]] = []

    for ch in sequence:
        if ch in draw_symbols:
            x2 = x + step * math.cos(heading)
            y2 = y + step * math.sin(heading)
            segs.append((x, y, x2, y2))
            x, y = x2, y2
        elif ch in move_symbols:
            x += step * math.cos(heading)
            y += step * math.sin(heading)
        elif ch == "+":
            heading += math.radians(angle_deg)
        elif ch == "-":
            heading -= math.radians(angle_deg)
        elif ch == "[":
            stack.append((x, y, heading))
        elif ch == "]":
            if stack:
                x, y, heading = stack.pop()
        # otros símbolos (X, Y, etc.) se ignoran a efectos gráficos

    return segs
