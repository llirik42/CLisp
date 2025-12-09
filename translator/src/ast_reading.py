from antlr4 import FileStream, CommonTokenStream, InputStream, StdinStream
from antlr4.error.ErrorListener import ErrorListener

from .LispLexer import LispLexer
from .LispParser import LispParser


__all__ = ["read_ast_from_file", "read_ast_from_stdin"]


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

def read_ast_from_file(input_file: str):
    """
    Reads the Lisp-code from the file and returns its AST.

    :param input_file: path to the Lisp-file.
    :raises SyntaxError: the file has syntax errors.
    :raises FileNotFoundError: the file not found.
    """

    return _read_ast(FileStream(input_file))


def read_ast_from_stdin():
    """
    Reads the Lisp-file from the stdin and returns its AST.
    """

    return _read_ast(StdinStream())


def read_ast(s: str):
    """
    Reads the Lisp-code from the stream and returns its AST.

    :param input_stream: stream with the code.
    :raises SyntaxError: the file has syntax errors.
    :raises FileNotFoundError: the file not found.
    """

    input_stream = InputStream(s)
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
