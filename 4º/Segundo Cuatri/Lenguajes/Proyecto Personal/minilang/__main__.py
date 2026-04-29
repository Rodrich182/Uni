import argparse
import sys
from pathlib import Path

from . import analyze_source, run_source
from .ast import flatten
from .errors import MiniLangError
from .lexer import MiniLangLexer


def main() -> int:
    cli = argparse.ArgumentParser(description="Intérprete del lenguaje MiniLang")
    cli.add_argument("path", help="Fichero fuente MiniLang")
    cli.add_argument("--tokens", action="store_true", help="Muestra la secuencia de tokens")
    cli.add_argument("--ast", action="store_true", help="Muestra el AST")
    cli.add_argument("--check", action="store_true", help="Solo analiza el programa sin ejecutarlo")
    args = cli.parse_args()

    source = Path(args.path).read_text(encoding="utf-8")

    try:
        if args.tokens:
            lexer = MiniLangLexer()
            for token in lexer.tokenize(source):
                print(f"{token.lineno:>3}  {token.type:<10} {token.value!r}")
            if not args.ast and not args.check:
                return 0

        program = analyze_source(source)

        if args.ast:
            for depth, node in flatten(program):
                indent = " " * (4 * depth)
                print(f"{indent}{node}")

        if args.check:
            print("Chequeo semántico completado correctamente.")

        if not args.tokens and not args.ast and not args.check:
            output = run_source(source)
            if output:
                print(output)
        return 0
    except MiniLangError as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
