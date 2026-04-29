from __future__ import annotations

from dataclasses import dataclass

from .ast import (
    Assignment,
    BinaryOp,
    Block,
    BooleanLiteral,
    Call,
    ExpressionStatement,
    FunctionDeclaration,
    IfStatement,
    IntegerLiteral,
    Name,
    NodeVisitor,
    PrintStatement,
    Program,
    ReturnStatement,
    UnaryOp,
    VarDeclaration,
    WhileStatement,
)
from .errors import semantic_error


BUILTIN_TYPES = {"int", "bool", "void"}


@dataclass
class VariableSymbol:
    name: str
    type_name: str


@dataclass
class FunctionSymbol:
    name: str
    parameter_types: list[str]
    return_type: str
    declaration: FunctionDeclaration


class Scope:
    def __init__(self, parent: "Scope | None" = None):
        self.parent = parent
        self.symbols: dict[str, VariableSymbol | FunctionSymbol] = {}

    def define(self, name: str, symbol):
        if name in self.symbols:
            return False
        self.symbols[name] = symbol
        return True

    def lookup_local(self, name: str):
        return self.symbols.get(name)

    def lookup(self, name: str):
        scope = self
        while scope is not None:
            symbol = scope.symbols.get(name)
            if symbol is not None:
                return symbol
            scope = scope.parent
        return None


class SemanticChecker(NodeVisitor):
    def __init__(self):
        self.global_scope = Scope()
        self.scope = self.global_scope
        self.current_function: FunctionSymbol | None = None

    def visit_Program(self, node: Program):
        for declaration in node.declarations:
            if isinstance(declaration, FunctionDeclaration):
                self._declare_function(declaration)

        for declaration in node.declarations:
            self.visit(declaration)

    def visit_FunctionDeclaration(self, node: FunctionDeclaration):
        symbol = self.global_scope.lookup_local(node.name)
        previous_scope = self.scope
        previous_function = self.current_function

        self.scope = Scope(self.global_scope)
        self.current_function = symbol

        for parameter, parameter_type in zip(node.parameters, symbol.parameter_types):
            if parameter_type == "void":
                semantic_error(getattr(parameter, "lineno", None), "a parameter cannot have type 'void'")
            if not self.scope.define(parameter.name, VariableSymbol(parameter.name, parameter_type)):
                semantic_error(getattr(parameter, "lineno", None), f"duplicate parameter '{parameter.name}'")
            parameter.type = parameter_type

        self.visit(node.body)

        self.current_function = previous_function
        self.scope = previous_scope

    def visit_Block(self, node: Block):
        previous_scope = self.scope
        self.scope = Scope(previous_scope)
        for statement in node.statements:
            self.visit(statement)
        self.scope = previous_scope

    def visit_VarDeclaration(self, node: VarDeclaration):
        declared_type = self._validate_type_name(node.type_name.name, node.type_name.lineno)
        if declared_type == "void":
            semantic_error(getattr(node, "lineno", None), "variables cannot have type 'void'")

        if self.scope.lookup_local(node.name) is not None:
            semantic_error(getattr(node, "lineno", None), f"'{node.name}' is already defined in this scope")

        if node.initializer is not None:
            self.visit(node.initializer)
            self._expect_same_type(declared_type, node.initializer.type, node.lineno, "initializer type mismatch")

        self.scope.define(node.name, VariableSymbol(node.name, declared_type))
        node.type = declared_type

    def visit_Assignment(self, node: Assignment):
        symbol = self.scope.lookup(node.name)
        if symbol is None:
            semantic_error(getattr(node, "lineno", None), f"unknown identifier '{node.name}'")
        if isinstance(symbol, FunctionSymbol):
            semantic_error(getattr(node, "lineno", None), f"cannot assign to function '{node.name}'")

        self.visit(node.value)
        self._expect_same_type(
            symbol.type_name,
            node.value.type,
            node.lineno,
            f"cannot assign {node.value.type} to {symbol.type_name}",
        )

    def visit_PrintStatement(self, node: PrintStatement):
        self.visit(node.expression)
        if node.expression.type == "void":
            semantic_error(getattr(node, "lineno", None), "cannot print the result of a void function")

    def visit_IfStatement(self, node: IfStatement):
        self.visit(node.condition)
        self._expect_same_type("bool", node.condition.type, node.lineno, "if condition must be boolean")
        self.visit(node.then_branch)
        if node.else_branch is not None:
            self.visit(node.else_branch)

    def visit_WhileStatement(self, node: WhileStatement):
        self.visit(node.condition)
        self._expect_same_type("bool", node.condition.type, node.lineno, "while condition must be boolean")
        self.visit(node.body)

    def visit_ReturnStatement(self, node: ReturnStatement):
        if self.current_function is None:
            semantic_error(getattr(node, "lineno", None), "return can only appear inside a function")

        expected = self.current_function.return_type
        if expected == "void":
            if node.value is not None:
                semantic_error(getattr(node, "lineno", None), "void functions cannot return a value")
            return

        if node.value is None:
            semantic_error(
                getattr(node, "lineno", None),
                f"function '{self.current_function.name}' must return a value of type {expected}",
            )

        self.visit(node.value)
        self._expect_same_type(expected, node.value.type, node.lineno, f"return type must be {expected}")

    def visit_ExpressionStatement(self, node: ExpressionStatement):
        self.visit(node.expression)

    def visit_IntegerLiteral(self, node: IntegerLiteral):
        node.type = "int"

    def visit_BooleanLiteral(self, node: BooleanLiteral):
        node.type = "bool"

    def visit_Name(self, node: Name):
        symbol = self.scope.lookup(node.identifier)
        if symbol is None:
            semantic_error(getattr(node, "lineno", None), f"unknown identifier '{node.identifier}'")
        if isinstance(symbol, FunctionSymbol):
            semantic_error(getattr(node, "lineno", None), f"function '{node.identifier}' must be called with parentheses")
        node.type = symbol.type_name

    def visit_UnaryOp(self, node: UnaryOp):
        self.visit(node.operand)
        if node.op == "-":
            self._expect_same_type("int", node.operand.type, node.lineno, "unary '-' expects an integer")
            node.type = "int"
            return
        if node.op == "not":
            self._expect_same_type("bool", node.operand.type, node.lineno, "'not' expects a boolean")
            node.type = "bool"
            return
        semantic_error(getattr(node, "lineno", None), f"unsupported unary operator '{node.op}'")

    def visit_BinaryOp(self, node: BinaryOp):
        self.visit(node.left)
        self.visit(node.right)

        arithmetic = {"+", "-", "*", "/", "%"}
        comparison = {"<", "<=", ">", ">="}
        equality = {"==", "!="}
        logical = {"and", "or"}

        if node.op in arithmetic:
            self._expect_same_type("int", node.left.type, node.lineno, f"left operand of '{node.op}' must be int")
            self._expect_same_type("int", node.right.type, node.lineno, f"right operand of '{node.op}' must be int")
            node.type = "int"
            return

        if node.op in comparison:
            self._expect_same_type("int", node.left.type, node.lineno, f"left operand of '{node.op}' must be int")
            self._expect_same_type("int", node.right.type, node.lineno, f"right operand of '{node.op}' must be int")
            node.type = "bool"
            return

        if node.op in equality:
            if node.left.type == "void" or node.right.type == "void":
                semantic_error(getattr(node, "lineno", None), "void values cannot be compared")
            self._expect_same_type(node.left.type, node.right.type, node.lineno, "both sides of an equality must share the same type")
            node.type = "bool"
            return

        if node.op in logical:
            self._expect_same_type("bool", node.left.type, node.lineno, f"left operand of '{node.op}' must be bool")
            self._expect_same_type("bool", node.right.type, node.lineno, f"right operand of '{node.op}' must be bool")
            node.type = "bool"
            return

        semantic_error(getattr(node, "lineno", None), f"unsupported operator '{node.op}'")

    def visit_Call(self, node: Call):
        symbol = self.scope.lookup(node.callee)
        if symbol is None:
            semantic_error(getattr(node, "lineno", None), f"unknown function '{node.callee}'")
        if isinstance(symbol, VariableSymbol):
            semantic_error(getattr(node, "lineno", None), f"'{node.callee}' is a variable, not a function")

        if len(node.arguments) != len(symbol.parameter_types):
            semantic_error(
                getattr(node, "lineno", None),
                f"function '{node.callee}' expects {len(symbol.parameter_types)} arguments but received {len(node.arguments)}",
            )

        for index, (argument, expected) in enumerate(zip(node.arguments, symbol.parameter_types), start=1):
            self.visit(argument)
            self._expect_same_type(expected, argument.type, node.lineno, f"argument {index} of '{node.callee}' must be {expected}")

        node.type = symbol.return_type

    def _declare_function(self, node: FunctionDeclaration):
        if self.global_scope.lookup_local(node.name) is not None:
            semantic_error(getattr(node, "lineno", None), f"'{node.name}' is already defined")

        parameter_types = []
        for parameter in node.parameters:
            parameter_types.append(self._validate_type_name(parameter.type_name.name, parameter.type_name.lineno))
        return_type = self._validate_type_name(node.return_type.name, node.return_type.lineno)

        symbol = FunctionSymbol(node.name, parameter_types, return_type, node)
        self.global_scope.define(node.name, symbol)
        node.type = return_type

    def _validate_type_name(self, type_name: str, lineno: int | None) -> str:
        if type_name not in BUILTIN_TYPES:
            semantic_error(lineno, f"unknown type '{type_name}'")
        return type_name

    def _expect_same_type(self, expected: str, received: str, lineno: int | None, message: str):
        if expected != received:
            semantic_error(lineno, f"{message}: expected {expected}, received {received}")


def check_program(program: Program) -> Program:
    checker = SemanticChecker()
    checker.visit(program)
    return program
