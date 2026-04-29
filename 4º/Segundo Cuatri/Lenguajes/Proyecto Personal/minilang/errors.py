class MiniLangError(Exception):
    """Base class for every compiler/interpreter error."""


class LexicalError(MiniLangError):
    """Raised when the lexer finds invalid input."""


class ParseError(MiniLangError):
    """Raised when the parser finds invalid syntax."""


class SemanticError(MiniLangError):
    """Raised during semantic analysis."""


class ExecutionError(MiniLangError):
    """Raised while executing a valid program."""


def _format(kind: str, lineno: int | None, message: str) -> str:
    if lineno is None:
        return f"{kind}: {message}"
    return f"{kind} [line {lineno}]: {message}"


def lexical_error(lineno: int | None, message: str) -> None:
    raise LexicalError(_format("Lexical error", lineno, message))


def parse_error(lineno: int | None, message: str) -> None:
    raise ParseError(_format("Syntax error", lineno, message))


def semantic_error(lineno: int | None, message: str) -> None:
    raise SemanticError(_format("Semantic error", lineno, message))


def execution_error(lineno: int | None, message: str) -> None:
    raise ExecutionError(_format("Runtime error", lineno, message))
