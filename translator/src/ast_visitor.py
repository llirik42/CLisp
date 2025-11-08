from LispParser import LispParser

from LispVisitor import LispVisitor
from procedures import *

__all__ = ["ASTVisitor"]


class ASTVisitor(LispVisitor):
    def __init__(self, procedure_table: ProcedureTable):
        self.__procedure_table = procedure_table

    def visitProgram(self, ctx: LispParser.ProgramContext):
        print(ctx.getText())
        return "123"
