from __future__ import annotations

import sys
import types
from typing import Any, Union, get_args, get_origin, get_type_hints


def _matches_type(value: Any, expected: Any) -> bool:
    if expected is Any:
        return True
    if expected is type(None):
        return value is None

    origin = get_origin(expected)
    if origin is list:
        if not isinstance(value, list):
            return False
        (item_type,) = get_args(expected)
        return all(_matches_type(item, item_type) for item in value)

    if origin in (Union, types.UnionType):
        return any(_matches_type(value, option) for option in get_args(expected))

    return isinstance(value, expected)


def _type_name(expected: Any) -> str:
    origin = get_origin(expected)
    if origin is list:
        (item_type,) = get_args(expected)
        return f"list[{_type_name(item_type)}]"
    if origin in (Union, types.UnionType):
        return " | ".join(_type_name(option) for option in get_args(expected))
    if expected is type(None):
        return "None"
    if expected is Any:
        return "Any"
    return getattr(expected, "__name__", repr(expected))


class AST:
    _fields: list[str] = []
    _field_types: dict[str, Any] = {}

    @classmethod
    def __init_subclass__(cls) -> None:
        raw_annotations = cls.__dict__.get("__annotations__", {})
        if not raw_annotations:
            cls._fields = []
            cls._field_types = {}
            return

        module = sys.modules[cls.__module__]
        resolved = get_type_hints(cls, globalns=vars(module), localns=dict(vars(module), **vars(cls)))
        cls._fields = list(raw_annotations)
        cls._field_types = {name: resolved[name] for name in cls._fields}

        def __init__(self, *args, **kwargs):
            if len(args) != len(cls._fields):
                raise TypeError(f"{cls.__name__} expected {len(cls._fields)} arguments, got {len(args)}")

            for field_name, value in zip(cls._fields, args):
                expected = cls._field_types[field_name]
                if not _matches_type(value, expected):
                    raise TypeError(
                        f"Field '{field_name}' of {cls.__name__} expected {_type_name(expected)}, "
                        f"got {type(value).__name__}"
                    )
                setattr(self, field_name, value)

            for key, value in kwargs.items():
                setattr(self, key, value)

        cls.__init__ = __init__

    def __repr__(self) -> str:
        parts = [f"{name}={getattr(self, name)!r}" for name in self._fields]
        return f"{type(self).__name__}({', '.join(parts)})"


class Declaration(AST):
    pass


class Statement(Declaration):
    pass


class Expression(AST):
    pass


class Program(AST):
    declarations: list[Declaration]


class TypeName(AST):
    name: str


class Parameter(AST):
    name: str
    type_name: TypeName


class Block(Statement):
    statements: list[Statement]


class FunctionDeclaration(Declaration):
    name: str
    parameters: list[Parameter]
    return_type: TypeName
    body: Block


class VarDeclaration(Statement):
    name: str
    type_name: TypeName
    initializer: Expression | None


class Assignment(Statement):
    name: str
    value: Expression


class PrintStatement(Statement):
    expression: Expression


class IfStatement(Statement):
    condition: Expression
    then_branch: Statement
    else_branch: Statement | None


class WhileStatement(Statement):
    condition: Expression
    body: Statement


class ReturnStatement(Statement):
    value: Expression | None


class ExpressionStatement(Statement):
    expression: Expression


class IntegerLiteral(Expression):
    value: int


class BooleanLiteral(Expression):
    value: bool


class Name(Expression):
    identifier: str


class BinaryOp(Expression):
    op: str
    left: Expression
    right: Expression


class UnaryOp(Expression):
    op: str
    operand: Expression


class Call(Expression):
    callee: str
    arguments: list[Expression]


class VisitDict(dict):
    def __setitem__(self, key, value):
        if key in self:
            raise AttributeError(f"Duplicate definition for {key}")
        super().__setitem__(key, value)


class NodeVisitMeta(type):
    @classmethod
    def __prepare__(cls, name, bases):
        return VisitDict()


class NodeVisitor(metaclass=NodeVisitMeta):
    def visit(self, node):
        if isinstance(node, list):
            for item in node:
                self.visit(item)
            return None
        if isinstance(node, AST):
            method = getattr(self, f"visit_{type(node).__name__}", self.generic_visit)
            return method(node)
        return node

    def generic_visit(self, node):
        for field in getattr(node, "_fields", []):
            self.visit(getattr(node, field))
        return None

    @classmethod
    def __init_subclass__(cls) -> None:
        for key in vars(cls):
            if key.startswith("visit_") and key[6:] not in globals():
                raise AssertionError(f"{key} does not match any AST node")


def flatten(top: AST) -> list[tuple[int, AST]]:
    class Flattener(NodeVisitor):
        def __init__(self):
            self.depth = 0
            self.nodes: list[tuple[int, AST]] = []

        def generic_visit(self, node):
            self.nodes.append((self.depth, node))
            self.depth += 1
            super().generic_visit(node)
            self.depth -= 1

    flattener = Flattener()
    flattener.visit(top)
    return flattener.nodes
