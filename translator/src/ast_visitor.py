from LispParser import LispParser

from LispVisitor import LispVisitor
from procedure_table import ProcedureTable

__all__ = ["ASTVisitor"]

from code_rendering import CodeCreator, Code

VisitResult = tuple[str, Code]


class ASTVisitor(LispVisitor):
    def __init__(
        self, procedure_table: ProcedureTable, template_creator: CodeCreator
    ):
        self.__procedure_table = procedure_table
        self.__template_creator = template_creator
        self.__variable_number = 0

    def visitProgram(self, ctx: LispParser.ProgramContext):
        templates = [self.visit(c)[1] for c in ctx.expression()]

        for t in templates:
            t.make_final()

        code = [t.render() for t in templates]
        return "\n".join(code)

    def visitProcedureCall(self, ctx: LispParser.ProcedureCallContext) -> VisitResult:
        template = self.__template_creator.procedure_call()

        lisp_function = ctx.operator().getText()

        c_function = self.__procedure_table.get_c_name(lisp_function)

        template.update_data(function=c_function)

        operands = ctx.operand()

        operand_names = []
        operand_templates: list[Code] = []

        for op in operands:
            op_name, op_template = self.visit(op)
            operand_names.append(op_name)
            operand_templates.append(op_template)

        template.update_data(args=operand_names)

        t0 = template
        variable_name = self.__create_variable_name()
        t0.update_data(var=variable_name)
        for t1 in operand_templates[::-1]:
            t1.add_code_pre(t0.render_pre())
            t1.add_code_post(t0.render_post())
            t0 = t1

        return variable_name, t0

    def visitBoolConstant(self, ctx: LispParser.BoolConstantContext) -> VisitResult:
        c_variable_name = self.__create_variable_name()
        template = self.__template_creator.make_boolean()
        value = 1 if ctx.getText() == "#t" else 0
        template.update_data(var=c_variable_name, value=value)
        return c_variable_name, template

    def visitStringConstant(self, ctx: LispParser.BoolConstantContext) -> VisitResult:
        c_variable_name = self.__create_variable_name()
        template = self.__template_creator.make_string()
        value = ctx.getText()
        template.update_data(var=c_variable_name, value=value)
        return c_variable_name, template

    def visitIntegerConstant(self, ctx: LispParser.BoolConstantContext) -> VisitResult:
        c_variable_name = self.__create_variable_name()
        template = self.__template_creator.make_int()
        value = int(ctx.getText())
        template.update_data(var=c_variable_name, value=value)
        return c_variable_name, template

    def __create_variable_name(self) -> str:
        self.__variable_number += 1
        return f"var{self.__variable_number}"
