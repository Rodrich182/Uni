from sly import Lexer

from .errors import lexical_error


class MiniLangLexer(Lexer):
    tokens = {
        LET,
        FUN,
        IF,
        ELSE,
        WHILE,
        RETURN,
        PRINT,
        TRUE,
        FALSE,
        INT,
        BOOL,
        VOID,
        AND,
        OR,
        NOT,
        ID,
        INTEGER,
        ARROW,
        EQ,
        NE,
        LE,
        GE,
        PLUS,
        MINUS,
        TIMES,
        DIVIDE,
        MOD,
        ASSIGN,
        LT,
        GT,
        LPAREN,
        RPAREN,
        LBRACE,
        RBRACE,
        COMMA,
        SEMI,
        COLON,
    }

    ignore = " \t\r"
    ignore_line_comment = r"//[^\n]*"

    ARROW = r"->"
    EQ = r"=="
    NE = r"!="
    LE = r"<="
    GE = r">="
    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIVIDE = r"/"
    MOD = r"%"
    ASSIGN = r"="
    LT = r"<"
    GT = r">"
    LPAREN = r"\("
    RPAREN = r"\)"
    LBRACE = r"\{"
    RBRACE = r"\}"
    COMMA = r","
    SEMI = r";"
    COLON = r":"

    @_(r"\d+")
    def INTEGER(self, token):
        token.value = int(token.value)
        return token

    ID = r"[A-Za-z_][A-Za-z0-9_]*"
    ID["let"] = LET
    ID["fun"] = FUN
    ID["if"] = IF
    ID["else"] = ELSE
    ID["while"] = WHILE
    ID["return"] = RETURN
    ID["print"] = PRINT
    ID["true"] = TRUE
    ID["false"] = FALSE
    ID["int"] = INT
    ID["bool"] = BOOL
    ID["void"] = VOID
    ID["and"] = AND
    ID["or"] = OR
    ID["not"] = NOT

    @_(r"/\*[\s\S]*?\*/")
    def block_comment(self, token):
        self.lineno += token.value.count("\n")

    @_(r"\n+")
    def newline(self, token):
        self.lineno += len(token.value)

    def error(self, token):
        lexical_error(self.lineno, f"illegal character {token.value[0]!r}")
