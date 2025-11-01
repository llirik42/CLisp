import sys
import uuid

from antlr4 import *

from LispLexer import LispLexer
from LispParser import LispParser
from LispVisitor import LispVisitor

class Visitor(LispVisitor):
    def visitNumber(self, ctx:LispParser.NumberContext) -> tuple[str, str, str]:
        variable_name = '_' + uuid.uuid4().hex
        create_code = f"Object* {variable_name} = make_int({ctx.getText()});"
        destroy_code = f"destroy({variable_name});"
        return variable_name, create_code, destroy_code

    def visitPrintExpr(self, ctx:LispParser.PrintExprContext) -> list[str]:
        number_code = self.visit(ctx.getChild(2))
        return [number_code[1], f"print({number_code[0]});", number_code[2]]

    def visitProgram(self, ctx:LispParser.ProgramContext):
        lines = [f"    {l}" for l in self.visit(ctx.getChild(0))]

        return f"""#include <stdio.h>
#include "runtime.h"
        
int main() {{
{"\n".join(lines)}
}}
"""

def main(argv):
    input_file = argv[1]
    output_file = argv[2]

    input_stream = FileStream(input_file)

    lexer = LispLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LispParser(stream)
    tree = parser.prog()

    visitor = Visitor()
    output = visitor.visit(tree)

    with open(output_file, "w") as f:
        f.write(output)

if __name__ == '__main__':
    main(sys.argv)
