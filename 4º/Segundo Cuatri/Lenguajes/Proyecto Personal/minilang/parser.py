from sly import Parser

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
    Parameter,
    PrintStatement,
    Program,
    ReturnStatement,
    TypeName,
    UnaryOp,
    VarDeclaration,
    WhileStatement,
)
from .errors import parse_error
from .lexer import MiniLangLexer


class MiniLangParser(Parser):
    tokens = MiniLangLexer.tokens

    precedence = (
        ("nonassoc", "IFX"),
        ("nonassoc", "ELSE"),
    )

    @_('declarations')
    def program(self, p):
        return Program(p.declarations, lineno=1)

    @_('declarations declaration')
    def declarations(self, p):
        return p.declarations + [p.declaration]

    @_('empty')
    def declarations(self, p):
        return []

    @_('function_declaration')
    def declaration(self, p):
        return p.function_declaration

    @_('statement')
    def declaration(self, p):
        return p.statement

    @_('FUN ID LPAREN parameters_opt RPAREN ARROW type_name block')
    def function_declaration(self, p):
        return FunctionDeclaration(p.ID, p.parameters_opt, p.type_name, p.block, lineno=p.lineno)

    @_('parameters')
    def parameters_opt(self, p):
        return p.parameters

    @_('empty')
    def parameters_opt(self, p):
        return []

    @_('parameters COMMA parameter')
    def parameters(self, p):
        return p.parameters + [p.parameter]

    @_('parameter')
    def parameters(self, p):
        return [p.parameter]

    @_('ID COLON type_name')
    def parameter(self, p):
        return Parameter(p.ID, p.type_name, lineno=p.lineno)

    @_('LET ID COLON type_name ASSIGN expression SEMI')
    def statement(self, p):
        return VarDeclaration(p.ID, p.type_name, p.expression, lineno=p.lineno)

    @_('LET ID COLON type_name SEMI')
    def statement(self, p):
        return VarDeclaration(p.ID, p.type_name, None, lineno=p.lineno)

    @_('ID ASSIGN expression SEMI')
    def statement(self, p):
        return Assignment(p.ID, p.expression, lineno=p.lineno)

    @_('PRINT expression SEMI')
    def statement(self, p):
        return PrintStatement(p.expression, lineno=p.lineno)

    @_('RETURN expression SEMI')
    def statement(self, p):
        return ReturnStatement(p.expression, lineno=p.lineno)

    @_('RETURN SEMI')
    def statement(self, p):
        return ReturnStatement(None, lineno=p.lineno)

    @_('IF LPAREN expression RPAREN statement ELSE statement')
    def statement(self, p):
        return IfStatement(p.expression, p.statement0, p.statement1, lineno=p.lineno)

    @_('IF LPAREN expression RPAREN statement %prec IFX')
    def statement(self, p):
        return IfStatement(p.expression, p.statement, None, lineno=p.lineno)

    @_('WHILE LPAREN expression RPAREN statement')
    def statement(self, p):
        return WhileStatement(p.expression, p.statement, lineno=p.lineno)

    @_('block')
    def statement(self, p):
        return p.block

    @_('expression SEMI')
    def statement(self, p):
        return ExpressionStatement(p.expression, lineno=getattr(p.expression, "lineno", p.lineno))

    @_('LBRACE statements RBRACE')
    def block(self, p):
        return Block(p.statements, lineno=p.lineno)

    @_('statements statement')
    def statements(self, p):
        return p.statements + [p.statement]

    @_('empty')
    def statements(self, p):
        return []

    @_('logical_or')
    def expression(self, p):
        return p.logical_or

    @_('logical_or OR logical_and')
    def logical_or(self, p):
        return BinaryOp("or", p.logical_or, p.logical_and, lineno=getattr(p.logical_or, "lineno", p.lineno))

    @_('logical_and')
    def logical_or(self, p):
        return p.logical_and

    @_('logical_and AND equality')
    def logical_and(self, p):
        return BinaryOp("and", p.logical_and, p.equality, lineno=getattr(p.logical_and, "lineno", p.lineno))

    @_('equality')
    def logical_and(self, p):
        return p.equality

    @_('equality EQ comparison')
    def equality(self, p):
        return BinaryOp("==", p.equality, p.comparison, lineno=getattr(p.equality, "lineno", p.lineno))

    @_('equality NE comparison')
    def equality(self, p):
        return BinaryOp("!=", p.equality, p.comparison, lineno=getattr(p.equality, "lineno", p.lineno))

    @_('comparison')
    def equality(self, p):
        return p.comparison

    @_('comparison LT term')
    def comparison(self, p):
        return BinaryOp("<", p.comparison, p.term, lineno=getattr(p.comparison, "lineno", p.lineno))

    @_('comparison LE term')
    def comparison(self, p):
        return BinaryOp("<=", p.comparison, p.term, lineno=getattr(p.comparison, "lineno", p.lineno))

    @_('comparison GT term')
    def comparison(self, p):
        return BinaryOp(">", p.comparison, p.term, lineno=getattr(p.comparison, "lineno", p.lineno))

    @_('comparison GE term')
    def comparison(self, p):
        return BinaryOp(">=", p.comparison, p.term, lineno=getattr(p.comparison, "lineno", p.lineno))

    @_('term')
    def comparison(self, p):
        return p.term

    @_('term PLUS factor')
    def term(self, p):
        return BinaryOp("+", p.term, p.factor, lineno=getattr(p.term, "lineno", p.lineno))

    @_('term MINUS factor')
    def term(self, p):
        return BinaryOp("-", p.term, p.factor, lineno=getattr(p.term, "lineno", p.lineno))

    @_('factor')
    def term(self, p):
        return p.factor

    @_('factor TIMES unary')
    def factor(self, p):
        return BinaryOp("*", p.factor, p.unary, lineno=getattr(p.factor, "lineno", p.lineno))

    @_('factor DIVIDE unary')
    def factor(self, p):
        return BinaryOp("/", p.factor, p.unary, lineno=getattr(p.factor, "lineno", p.lineno))

    @_('factor MOD unary')
    def factor(self, p):
        return BinaryOp("%", p.factor, p.unary, lineno=getattr(p.factor, "lineno", p.lineno))

    @_('unary')
    def factor(self, p):
        return p.unary

    @_('MINUS unary')
    def unary(self, p):
        return UnaryOp("-", p.unary, lineno=p.lineno)

    @_('NOT unary')
    def unary(self, p):
        return UnaryOp("not", p.unary, lineno=p.lineno)

    @_('call')
    def unary(self, p):
        return p.call

    @_('ID LPAREN arguments_opt RPAREN')
    def call(self, p):
        return Call(p.ID, p.arguments_opt, lineno=p.lineno)

    @_('primary')
    def call(self, p):
        return p.primary

    @_('arguments')
    def arguments_opt(self, p):
        return p.arguments

    @_('empty')
    def arguments_opt(self, p):
        return []

    @_('arguments COMMA expression')
    def arguments(self, p):
        return p.arguments + [p.expression]

    @_('expression')
    def arguments(self, p):
        return [p.expression]

    @_('INTEGER')
    def primary(self, p):
        return IntegerLiteral(p.INTEGER, lineno=p.lineno)

    @_('TRUE')
    def primary(self, p):
        return BooleanLiteral(True, lineno=p.lineno)

    @_('FALSE')
    def primary(self, p):
        return BooleanLiteral(False, lineno=p.lineno)

    @_('ID')
    def primary(self, p):
        return Name(p.ID, lineno=p.lineno)

    @_('LPAREN expression RPAREN')
    def primary(self, p):
        return p.expression

    @_('INT')
    def type_name(self, p):
        return TypeName("int", lineno=p.lineno)

    @_('BOOL')
    def type_name(self, p):
        return TypeName("bool", lineno=p.lineno)

    @_('VOID')
    def type_name(self, p):
        return TypeName("void", lineno=p.lineno)

    @_('')
    def empty(self, p):
        return []

    def error(self, token):
        if token is None:
            parse_error(None, "unexpected end of file")
        parse_error(token.lineno, f"unexpected token {token.type!r} with value {token.value!r}")


def parse_source(source: str):
    lexer = MiniLangLexer()
    parser = MiniLangParser()
    return parser.parse(lexer.tokenize(source))
