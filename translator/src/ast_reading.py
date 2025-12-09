from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from .LispLexer import LispLexer
from .LispParser import LispParser


class CustomErrorListener(ErrorListener):
    def __init__(self):
        super(CustomErrorListener, self).__init__()
        self.__error = ""

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        """
        Handler of the syntax error.
        """

        self.__error = f"line {line}:{column} {msg}"

    @property
    def error(self):
        """
        Text of the syntax error.
        """

        return self.__error


def read_ast(code: str):
    """
    Reads the Lisp-code from the stream and returns its AST.

    :param code: code.
    :raises SyntaxError: the file has syntax errors.
    :raises FileNotFoundError: the file not found.
    """

    input_stream = InputStream(code)
    lexer = LispLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LispParser(stream)
    parser.removeErrorListeners()

    listener = CustomErrorListener()
    parser.addErrorListener(listener)

    res = parser.program()

    if parser.getNumberOfSyntaxErrors() > 0:
        raise SyntaxError(listener.error)

    return res
