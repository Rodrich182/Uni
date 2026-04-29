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
    PrintStatement,
    Program,
    ReturnStatement,
    UnaryOp,
    VarDeclaration,
    WhileStatement,
)
from .errors import execution_error


class Environment:
    def __init__(self, parent: "Environment | None" = None):
        self.parent = parent
        self.values: dict[str, object] = {}

    def define(self, name: str, value):
        self.values[name] = value

    def get(self, name: str):
        if name in self.values:
            return self.values[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise KeyError(name)

    def assign(self, name: str, value):
        if name in self.values:
            self.values[name] = value
            return
        if self.parent is not None:
            self.parent.assign(name, value)
            return
        raise KeyError(name)


@dataclass
class FunctionValue:
    declaration: FunctionDeclaration
    closure: Environment


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class Interpreter:
    def __init__(self):
        self.output: list[str] = []
        self.globals = Environment()

    def interpret(self, program: Program) -> str:
        for declaration in program.declarations:
            if isinstance(declaration, FunctionDeclaration):
                self.globals.define(declaration.name, FunctionValue(declaration, self.globals))

        for declaration in program.declarations:
            if not isinstance(declaration, FunctionDeclaration):
                self.execute(declaration, self.globals)

        return "\n".join(self.output)

    def execute(self, node, env: Environment):
        method = getattr(self, f"exec_{type(node).__name__}")
        return method(node, env)

    def evaluate(self, node, env: Environment):
        method = getattr(self, f"eval_{type(node).__name__}")
        return method(node, env)

    def exec_Block(self, node: Block, env: Environment):
        local = Environment(env)
        for statement in node.statements:
            self.execute(statement, local)

    def exec_VarDeclaration(self, node: VarDeclaration, env: Environment):
        if node.initializer is None:
            value = self._default_value(node.type_name.name)
        else:
            value = self.evaluate(node.initializer, env)
        env.define(node.name, value)

    def exec_Assignment(self, node: Assignment, env: Environment):
        value = self.evaluate(node.value, env)
        try:
            env.assign(node.name, value)
        except KeyError:
            execution_error(getattr(node, "lineno", None), f"unknown identifier '{node.name}'")

    def exec_PrintStatement(self, node: PrintStatement, env: Environment):
        value = self.evaluate(node.expression, env)
        self.output.append(self._format_value(value))

    def exec_IfStatement(self, node: IfStatement, env: Environment):
        if self.evaluate(node.condition, env):
            self.execute(node.then_branch, env)
        elif node.else_branch is not None:
            self.execute(node.else_branch, env)

    def exec_WhileStatement(self, node: WhileStatement, env: Environment):
        while self.evaluate(node.condition, env):
            self.execute(node.body, env)

    def exec_ReturnStatement(self, node: ReturnStatement, env: Environment):
        value = None if node.value is None else self.evaluate(node.value, env)
        raise ReturnSignal(value)

    def exec_ExpressionStatement(self, node: ExpressionStatement, env: Environment):
        self.evaluate(node.expression, env)

    def eval_IntegerLiteral(self, node: IntegerLiteral, env: Environment):
        return node.value

    def eval_BooleanLiteral(self, node: BooleanLiteral, env: Environment):
        return node.value

    def eval_Name(self, node: Name, env: Environment):
        try:
            return env.get(node.identifier)
        except KeyError:
            execution_error(getattr(node, "lineno", None), f"unknown identifier '{node.identifier}'")

    def eval_UnaryOp(self, node: UnaryOp, env: Environment):
        value = self.evaluate(node.operand, env)
        if node.op == "-":
            return -value
        if node.op == "not":
            return not value
        execution_error(getattr(node, "lineno", None), f"unsupported unary operator '{node.op}'")

    def eval_BinaryOp(self, node: BinaryOp, env: Environment):
        left = self.evaluate(node.left, env)
        right = self.evaluate(node.right, env)

        try:
            if node.op == "+":
                return left + right
            if node.op == "-":
                return left - right
            if node.op == "*":
                return left * right
            if node.op == "/":
                return left // right
            if node.op == "%":
                return left % right
            if node.op == "<":
                return left < right
            if node.op == "<=":
                return left <= right
            if node.op == ">":
                return left > right
            if node.op == ">=":
                return left >= right
            if node.op == "==":
                return left == right
            if node.op == "!=":
                return left != right
            if node.op == "and":
                return left and right
            if node.op == "or":
                return left or right
        except ZeroDivisionError:
            execution_error(getattr(node, "lineno", None), "division by zero")

        execution_error(getattr(node, "lineno", None), f"unsupported operator '{node.op}'")

    def eval_Call(self, node: Call, env: Environment):
        try:
            function = env.get(node.callee)
        except KeyError:
            execution_error(getattr(node, "lineno", None), f"unknown function '{node.callee}'")

        if not isinstance(function, FunctionValue):
            execution_error(getattr(node, "lineno", None), f"'{node.callee}' is not callable")

        arguments = [self.evaluate(argument, env) for argument in node.arguments]
        return self._call_function(function, arguments)

    def _call_function(self, function: FunctionValue, arguments: list[object]):
        declaration = function.declaration
        local = Environment(function.closure)

        for parameter, value in zip(declaration.parameters, arguments):
            local.define(parameter.name, value)

        try:
            self.execute(declaration.body, local)
        except ReturnSignal as signal:
            return signal.value

        if declaration.return_type.name == "void":
            return None
        execution_error(getattr(declaration, "lineno", None), f"function '{declaration.name}' ended without returning a value")

    def _default_value(self, type_name: str):
        if type_name == "int":
            return 0
        if type_name == "bool":
            return False
        return None

    def _format_value(self, value):
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)


def run_program(program: Program) -> str:
    return Interpreter().interpret(program)
