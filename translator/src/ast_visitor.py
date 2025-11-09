from typing import Union

from LispParser import LispParser

from LispVisitor import LispVisitor
from procedure_table import ProcedureTable

from code_rendering import CodeCreator, Code


__all__ = ["ASTVisitor"]


VisitResult = tuple[str, Code]


class ASTVisitor(LispVisitor):
    def __init__(self, procedure_table: ProcedureTable, code_creator: CodeCreator):
        self.__procedure_table = procedure_table
        self.__code_creator = code_creator
        self.__variable_number = 0  # Number of the previously declared variable

    def visitProgram(self, ctx: LispParser.ProgramContext):
        final_codes = [self.visit(e)[1] for e in ctx.expression()]
        for t in final_codes:
            t.make_final()
        final_codes_rendered = [c.render() for c in final_codes]

        top_level_code = self.__code_creator.main_function()
        top_level_code.update_data(code="\n".join(final_codes_rendered))

        return top_level_code.render()

    def visitProcedureCall(self, ctx: LispParser.ProcedureCallContext) -> VisitResult:
        # Getting name of the procedure
        lisp_function = ctx.operator().getText()
        c_function = self.__procedure_table.get_c_func(lisp_function)

        # Code of the current visiting expression (procedure call)
        code = self.__code_creator.procedure_call()
        code.update_data(function=c_function)

        # Visit all operands
        operand_variable_names, operand_codes = self.__visit_operands(ctx.operand())

        # Create variable name for the current expression
        c_variable_name = self.__create_variable_name()

        # Update data must be before wrapping, so that the wrapped code contains all the data
        code.update_data(args=operand_variable_names, var=c_variable_name)
        code = self.__wrap_code_into_operands(
            start_code=code, operand_codes=operand_codes
        )

        return c_variable_name, code

    def visitBoolConstant(self, ctx: LispParser.BoolConstantContext) -> VisitResult:
        return self.__visit_constant(
            code=self.__code_creator.make_boolean(),
            value=1 if ctx.getText() == "#t" else 0,
        )

    def visitStringConstant(self, ctx: LispParser.BoolConstantContext) -> VisitResult:
        return self.__visit_constant(
            code=self.__code_creator.make_string(), value=ctx.getText()
        )

    def visitIntegerConstant(self, ctx: LispParser.BoolConstantContext) -> VisitResult:
        return self.__visit_constant(
            code=self.__code_creator.make_int(), value=int(ctx.getText())
        )

    def __create_variable_name(self) -> str:
        self.__variable_number += 1
        return f"var{self.__variable_number}"

    def __visit_constant(self, code: Code, value: Union[str, int]) -> VisitResult:
        c_variable_name = self.__create_variable_name()
        code.update_data(var=c_variable_name, value=value)
        return c_variable_name, code

    def __visit_operands(self, operands) -> tuple[list[str], list[Code]]:
        operand_names = []
        operand_codes = []

        for op in operands:
            op_name, op_template = self.visit(op)
            operand_names.append(op_name)
            operand_codes.append(op_template)

        return operand_names, operand_codes

    @staticmethod
    def __wrap_code_into_operands(start_code: Code, operand_codes: list[Code]) -> Code:
        code = start_code

        for operand_code in operand_codes[::-1]:
            operand_code.add_main_epilog(start_code.render_main())
            operand_code.add_secondary_prolog(code.render_secondary())
            code = operand_code

        return code
