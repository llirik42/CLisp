from typing import Union

from src.LispParser import LispParser
from src.LispVisitor import LispVisitor
from src.code_rendering import CodeCreator, Code, C_IF
from src.procedure_table import ProcedureTable
from .context import ConditionVisitingContext
from .exceptions import VisitingException
from .variable_manager import VariableManager


__all__ = ["ASTVisitor"]


VisitResult = tuple[str, Code]


class ASTVisitor(LispVisitor):
    def __init__(
        self,
        procedure_table: ProcedureTable,
        code_creator: CodeCreator,
        variable_manager: VariableManager,
    ):
        """
        Class represents a visitor of AST of the Lisp. Result of the visiting - code on C, that can be used in interpretation.

        :param procedure_table: procedure table.
        :param code_creator: code creator.
        :param variable_manager: variable manager.
        """

        self.__procedure_table = procedure_table
        self.__code_creator = code_creator
        self.__variable_manager = variable_manager
        self.__condition_visiting_ctx = ConditionVisitingContext()

    def visitProgram(self, ctx: LispParser.ProgramContext):
        final_codes = [self.visit(e)[1] for e in ctx.expression()]
        for c in final_codes:
            c.make_final()
        final_codes_rendered = [c.render() for c in final_codes]

        main_function_code = self.__code_creator.main_function()
        main_function_code.update_data(code="\n".join(final_codes_rendered))

        return main_function_code.render()

    def visitCondition(self, ctx: LispParser.ConditionContext) -> VisitResult:
        test = ctx.test()
        consequent = ctx.consequent()
        alternate = ctx.alternate()

        test_name, test_code = self.visit(test)
        with self.__condition_visiting_ctx:
            consequent_name, consequent_code = self.visit(consequent)

        operand_names = [test_name, consequent_name]
        operand_codes = [test_code, consequent_code]

        if alternate is not None:
            with self.__condition_visiting_ctx:
                alternate_name, alternate_code = self.visit(alternate)
            operand_names.append(alternate_name)
            operand_codes.append(alternate_code)

        return self.__visit_function(
            function_name=C_IF, operand_names=operand_names, operand_codes=operand_codes
        )

    def visitProcedureCall(self, ctx: LispParser.ProcedureCallContext) -> VisitResult:
        lisp_function = ctx.operator().getText()
        c_function = self.__procedure_table.get_c_func(lisp_function)

        if c_function is None:
            raise VisitingException(
                message=f'Operator "{lisp_function}" not found!', ctx=ctx
            )

        operand_names, operand_codes = self.__visit_operands(ctx.operand())

        return self.__visit_function(c_function, operand_names, operand_codes)

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

    def __visit_constant(self, code: Code, value: Union[str, int]) -> VisitResult:
        expr_var_name = self.__variable_manager.create_variable_name()
        code.update_data(var=expr_var_name, value=value)
        return expr_var_name, code

    def __visit_function(
        self, function_name: str, operand_names: list[str], operand_codes: list[Code]
    ) -> VisitResult:
        if self.__condition_visiting_ctx.visiting:
            expr_code = self.__code_creator.make_evaluable()
        else:
            expr_code = self.__code_creator.function_call()

        expr_var_name = self.__variable_manager.create_variable_name()
        expr_code.update_data(
            function=function_name, args=operand_names, var=expr_var_name
        )
        wrapped_expr_code = self.__wrap_code(
            start_code=expr_code, wrapping_codes=operand_codes
        )

        return expr_var_name, wrapped_expr_code

    def __visit_operands(self, operands) -> tuple[list[str], list[Code]]:
        operand_names = []
        operand_codes = []

        for op in operands:
            op_name, op_template = self.visit(op)
            operand_names.append(op_name)
            operand_codes.append(op_template)

        return operand_names, operand_codes

    @staticmethod
    def __wrap_code(start_code: Code, wrapping_codes: list[Code]) -> Code:
        code = start_code

        for c in wrapping_codes[::-1]:
            c.add_main_epilog(code.render_main())
            c.add_secondary_prolog(code.render_secondary())
            code = c

        return code
