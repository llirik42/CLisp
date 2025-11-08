import sys
import uuid

from antlr4 import *

from LispLexer import LispLexer
from LispParser import LispParser
from LispVisitor import LispVisitor

class Visitor(LispVisitor):
    def visitProgram(self, ctx:LispParser.ProgramContext):
        print(ctx.getText())

def main(argv):
    input_file = argv[1]
    output_file = argv[2]

    input_stream = FileStream(input_file)

    lexer = LispLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LispParser(stream)
    tree = parser.program()

    visitor = Visitor()
    visitor.visit(tree)


if __name__ == '__main__':
    main(sys.argv)
