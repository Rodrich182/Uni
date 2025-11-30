# lsystems/presets.py

from dataclasses import dataclass
from typing import Dict

from dictionary import DEFAULT_LSYS_ANGLE, DEFAULT_LSYS_LENGTH


@dataclass(frozen=True)
class LSystemPreset:
    key: str
    name: str
    axiom: str
    rules: Dict[str, str]
    default_angle: float
    default_length: float
    description: str
    natural_phenomenon: str


PRESETS: Dict[str, LSystemPreset] = {
    "koch": LSystemPreset(
        key="koch",
        name="Curva de Koch",
        axiom="F",
        rules={
            "F": "F+F--F+F",
        },
        default_angle=60.0,
        default_length=DEFAULT_LSYS_LENGTH,
        description=(
            "L-sistema determinista de tipo DOL que genera la clásica curva de Koch."
        ),
        natural_phenomenon=(
            "Ejemplo de curva fractal con autosimilaridad, útil para estudiar "
            "fronteras y rugosidad en gráficos por computador."
        ),
    ),
    "sierpinski": LSystemPreset(
        key="sierpinski",
        name="Triángulo de Sierpinski",
        axiom="F-G-G",
        rules={
            "F": "F-G+F+G-F",
            "G": "GG-F-G+G+F-G",
        },
        default_angle=120.0,
        default_length=DEFAULT_LSYS_LENGTH,
        description=(
            "L-sistema determinista de dos símbolos (F y G) que genera el "
            "triángulo de Sierpinski."
        ),
        natural_phenomenon=(
            "Modelo idealizado de patrones triangulares autosimilares."
        ),
    ),
    "dragon": LSystemPreset(
        key="dragon",
        name="Curva del dragón",
        axiom="FX",
        rules={
            "X": "X+YF+",
            "Y": "-FX-Y",
        },
        default_angle=90.0,
        default_length=DEFAULT_LSYS_LENGTH,
        description=(
            "L-sistema determinista que produce la curva del dragón de Heighway."
        ),
        natural_phenomenon=(
            "Curva de relleno parcial del plano, usada como ejemplo de curvas "
            "fractalmente complejas."
        ),
    ),
    "planta": LSystemPreset(
        key="planta",
        name="Planta ramificada",
        axiom="F",
        rules={
            "F": "F[+F]F[-F]F",
        },
        default_angle=25.0,
        default_length=DEFAULT_LSYS_LENGTH,
        description=(
            "L-sistema con corchetes que genera una planta ramificada simple."
        ),
        natural_phenomenon=(
            "Simula el crecimiento de una planta con ramas laterales; los "
            "corchetes guardan y restauran el estado de la tortuga."
        ),
    ),
}
