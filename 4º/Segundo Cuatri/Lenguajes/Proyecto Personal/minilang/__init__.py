from pathlib import Path

from .checker import check_program
from .interpreter import run_program
from .parser import parse_source


def analyze_source(source: str):
    program = parse_source(source)
    return check_program(program)


def run_source(source: str) -> str:
    program = analyze_source(source)
    return run_program(program)


def run_file(path: str | Path) -> str:
    return run_source(Path(path).read_text(encoding="utf-8"))
