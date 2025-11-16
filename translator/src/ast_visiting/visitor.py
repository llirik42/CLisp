from typing import Union

from src.LispParser import LispParser
from src.LispVisitor import LispVisitor
from src.code_rendering import CodeCreator, Code, wrap_codes, nest_codes
from src.function_table import FunctionTable
from .context import EvaluableMakingContext
from .exceptions import VisitingException
from src.variable_manager import VariableManager


__all__ = ["ASTVisitor"]


VisitResult = tuple[str, Code]


class ASTVisitor(LispVisitor):
    def __init__(
        self,
        function_table: FunctionTable,
        code_creator: CodeCreator,
        variable_manager: VariableManager,
    ):
        """
        Class represents a visitor of AST of the Lisp. Result of the visiting - code on C, that can be used in interpretation.

        :param function_table: function table.
        :param code_creator: code creator.
        :param variable_manager: variable manager.
        """

        self.__function_table = function_table
        self.__code_creator = code_creator
        self.__variable_manager = variable_manager
        self.__condition_visiting_ctx = EvaluableMakingContext()
        self.__env = {
            "prev": {},
            "var": "global_env", #TODO: Отбить
            "variables": {}
        }


    def visitProgram(self, ctx: LispParser.ProgramContext) -> str:
        # Visit definitions

        definitions_codes = []
        for d in ctx.definition():
            definitions_codes.append(self.visit(d))

        global_env_name = "global_env" # TODO: отбить через manager
        global_env_code = self.__code_creator.make_environment(var=global_env_name, parentEnv="NULL") # TODO: вынести NULL (а лучше прямо в шаблоне это сделать)
        t = nest_codes([global_env_code] + definitions_codes)
        t.make_final()

        final_codes = [self.visit(e)[1] for e in ctx.expression()]
        for c in final_codes:
            c.make_final()
        final_codes_rendered = [c.render() for c in final_codes]

        t.add_main_epilog("\n" + "\n".join(final_codes_rendered) + "\n")

        main_function_code = self.__code_creator.main_function(
            code=t.render()
        )

        return main_function_code.render()

    def visitDefinition(self, ctx:LispParser.DefinitionContext) -> Code:
        variable = ctx.variable()
        # TODO: проверить, что нет коллизии с названием функций (variable)

        expression = ctx.expression()

        expr_name, expr_code = self.visit(expression)

        self.__env["variables"][variable.getText()] = expr_name

        code = self.__code_creator.set_variable_value(
            env=self.__env["var"],
            name=f"\"{variable.getText()}\"",
            value=expr_name
        )

        return wrap_codes([code, expr_code])

    def visitVariable(self, ctx:LispParser.VariableContext) -> VisitResult:
        variable = ctx.getText()

        # TODO: handle situation when variable is a standard-library function (like '+')

        if variable not in self.__env["variables"]:
            raise VisitingException(message=f"Unexpected variable \"{variable}\"", ctx=ctx)

        name = self.__env["variables"][variable]

        expr_name = self.__variable_manager.create_variable_name()
        expr_code = self.__code_creator.get_variable_value(var=expr_name, env=self.__env["var"], name=f"\"{variable}\"")

        return expr_name, expr_code

    def visitCondition(self, ctx: LispParser.ConditionContext) -> VisitResult:
        identifier = "if"
        c_function = self.__function_table.get_c_func(identifier)

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
            function_name=c_function,
            operand_names=operand_names,
            operand_codes=operand_codes,
        )

    def visitAnd(self, ctx: LispParser.AndContext) -> VisitResult:
        identifier = "and"
        c_function = self.__function_table.get_c_func(identifier)

        with self.__condition_visiting_ctx:
            operand_names, operand_codes = self.__visit_operands(ctx.test())

        return self.__visit_function(
            function_name=c_function,
            operand_names=operand_names,
            operand_codes=operand_codes,
        )

    def visitOr(self, ctx: LispParser.OrContext) -> VisitResult:
        identifier = "or"
        c_function = self.__function_table.get_c_func(identifier)

        with self.__condition_visiting_ctx:
            operand_names, operand_codes = self.__visit_operands(ctx.test())

        return self.__visit_function(
            function_name=c_function,
            operand_names=operand_names,
            operand_codes=operand_codes,
        )

    def visitProcedureCall(self, ctx: LispParser.ProcedureCallContext) -> VisitResult:
        lisp_function = ctx.operator().getText()

        try:
            c_function = self.__function_table.get_c_func(lisp_function)
        except ValueError as e:
            raise VisitingException(
                message=f'Operator "{lisp_function}" not found!', ctx=ctx
            ) from e

        operand_names, operand_codes = self.__visit_operands(ctx.operand())

        return self.__visit_function(
            function_name=c_function,
            operand_names=operand_names,
            operand_codes=operand_codes,
        )

    def visitBoolConstant(self, ctx: LispParser.BoolConstantContext) -> VisitResult:
        c_function = self.__function_table.get_c_func("#boolean#")

        code = self.__code_creator.make_constant(function=c_function)
        value = 1 if ctx.getText() == "#t" else 0

        return self.__visit_constant(
            code=code,
            value=value,
        )

    def visitCharacterConstant(
        self, ctx: LispParser.CharacterConstantContext
    ) -> VisitResult:
        value = f"{ctx.getText()[2:]}"

        if value == "'":
            value = "\\'"  # Escape single quote

        c_function = self.__function_table.get_c_func("#character#")
        code = self.__code_creator.make_constant(function=c_function)

        return self.__visit_constant(code=code, value=f"'{value}'")

    def visitStringConstant(self, ctx: LispParser.StringConstantContext) -> VisitResult:
        c_function = self.__function_table.get_c_func("#string#")
        code = self.__code_creator.make_constant(function=c_function)

        return self.__visit_constant(code=code, value=ctx.getText())

    def visitIntegerConstant(
        self, ctx: LispParser.IntegerConstantContext
    ) -> VisitResult:
        c_function = self.__function_table.get_c_func("#integer#")
        code = self.__code_creator.make_constant(function=c_function)

        return self.__visit_constant(code=code, value=int(ctx.getText()))

    def visitFloatConstant(self, ctx: LispParser.FloatConstantContext) -> VisitResult:
        c_function = self.__function_table.get_c_func("#float#")
        code = self.__code_creator.make_constant(function=c_function)

        return self.__visit_constant(code=code, value=float(ctx.getText()))

    def __visit_constant(
        self, code: Code, value: Union[str, int, float]
    ) -> VisitResult:
        expr_var_name = self.__variable_manager.create_variable_name()
        code.update_data(var=expr_var_name, value=value)

        return expr_var_name, code

    def __visit_function(
        self, function_name: str, operand_names: list[str], operand_codes: list[Code]
    ) -> VisitResult:
        if self.__condition_visiting_ctx.should_make_evaluable:
            expr_code = self.__code_creator.make_evaluable()
        else:
            expr_code = self.__code_creator.function_call()

        expr_var_name = self.__variable_manager.create_variable_name()
        expr_code.update_data(
            function=function_name, args=operand_names, var=expr_var_name
        )
        wrapped_expr_code = wrap_codes([expr_code] + operand_codes)

        return expr_var_name, wrapped_expr_code

    def __visit_operands(self, operands) -> tuple[list[str], list[Code]]:
        operand_names = []
        operand_codes = []

        for op in operands:
            op_name, op_template = self.visit(op)
            operand_names.append(op_name)
            operand_codes.append(op_template)

        return operand_names, operand_codes
