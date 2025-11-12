from typing import Union

from antlr4 import ParserRuleContext

from LispParser import LispParser

from LispVisitor import LispVisitor
from procedure_table import ProcedureTable

from code_rendering import CodeCreator, Code

from variable_manager import VariableManager


__all__ = ["ASTVisitor"]


class VisitingException(Exception):
    def __init__(self, message: str, ctx: ParserRuleContext):
        super().__init__(f"{message} [{ctx.getText()}]")
        self.__ctx = ctx

    @property
    def ctx(self) -> ParserRuleContext:
        return self.__ctx


VisitResult = tuple[str, Code]
C_NULL = "NULL"


class EvaluableVisitingContext:
    def __init__(self):
        self.__f = False


    def __enter__(self):
        self.__f = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__f = False

    @property
    def f(self):
        return self.__f



class ASTVisitor(LispVisitor):
    def __init__(
        self,
        procedure_table: ProcedureTable,
        code_creator: CodeCreator,
        variable_manager: VariableManager,
    ):
        self.__procedure_table = procedure_table
        self.__code_creator = code_creator
        self.__variable_manager = variable_manager
        self.__ctx = EvaluableVisitingContext()

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

        with self.__ctx:
            consequent_name, consequent_code = self.visit(consequent)


        expr_code = self.__code_creator.condition()
        expr_code.update_data(
            test=test_name,
            consequent=consequent_name,
            alternate=C_NULL,
        )
        wrapping_codes = [test_code, consequent_code]

        if alternate is None:
            alternate_name = self.__variable_manager.create_variable_name()
            alternate_code = self.__code_creator.make_unspecified()
            alternate_code.update_data(var=alternate_name)
            expr_code.update_data(alternate=alternate_name)
            wrapping_codes.append(alternate_code)
        else:
            with self.__ctx:
                alternate_name, alternate_code = self.visit(alternate)
            expr_code.update_data(alternate=alternate_name)
            wrapping_codes.append(alternate_code)

        expr_var_name = self.__variable_manager.create_variable_name()
        expr_code.update_data(var=expr_var_name)

        expr_code = self.__wrap_code(
            start_code=expr_code, wrapping_codes=wrapping_codes
        )

        return expr_var_name, expr_code

    def visitProcedureCall(self, ctx: LispParser.ProcedureCallContext) -> VisitResult:
        lisp_function = ctx.operator().getText()
        c_function = self.__procedure_table.get_c_func(lisp_function)

        if c_function is None:
            raise VisitingException(
                message=f'Operator "{lisp_function}" not found!', ctx=ctx
            )

        if self.__ctx.f:
            expr_code = self.__code_creator.make_evaluable()
        else:
            expr_code = self.__code_creator.procedure_call()

        expr_code.update_data(function=c_function)

        operand_variable_names, operand_codes = self.__visit_operands(ctx.operand())

        expr_var_name = self.__variable_manager.create_variable_name()

        expr_code.update_data(args=operand_variable_names, var=expr_var_name)
        expr_code = self.__wrap_code(start_code=expr_code, wrapping_codes=operand_codes)

        return expr_var_name, expr_code

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
