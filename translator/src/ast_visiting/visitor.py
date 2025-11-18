from typing import Union

from src.LispParser import LispParser
from src.LispVisitor import LispVisitor
from src.code_rendering import CodeCreator, Code, wrap_codes, join_codes
from src.function_table import FunctionTable
from src.variable_manager import VariableManager
from .context import EvaluableMakingContext
from .exceptions import VisitingException


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
        self.__env = None

    @staticmethod
    def __has_variable(env: dict, name: str) -> bool:
        if name in env["variables"]:
            return True

        if len(env["prev"]) > 0:
            return ASTVisitor.__has_variable(env["prev"], name)

        return False

    @staticmethod
    def __update_variable(env: dict, name: str, new_value: str) -> None:
        if name in env["variables"]:
            env["variables"][name] = new_value
            return

        ASTVisitor.__update_variable(env["prev"], name, new_value)

    def visitProgram(self, ctx: LispParser.ProgramContext) -> str:
        self.__env = {
            "prev": {},
            "var": self.__variable_manager.create_environment_name(),
            "variables": {},
        }  # TODO: Отбить

        # Visit definitions

        global_env_code = self.__code_creator.make_environment(
            var=self.__env["var"], parentEnv="NULL"
        )

        self.__env["code"] = global_env_code

        codes = [self.visit(e)[1] for e in ctx.programElement()]
        for c in codes:
            c.make_final()

        global_env_code.update_data(varCount=len(self.__env["variables"]))
        global_env_code.add_main_epilog("\n" + join_codes(codes))

        main_function_code = self.__code_creator.main_function(
            code=global_env_code.render() + "\n"
        )
        main_function_code.make_final()

        return main_function_code.render()

    def visitDefinition(self, ctx: LispParser.DefinitionContext) -> VisitResult:
        variable = ctx.variable()
        # TODO: проверить, что нет коллизии с названием функций (variable)

        expression = ctx.expression()

        expr_name, expr_code = self.visit(expression)

        self.__env["code"].add_secondary_prolog(expr_code.render_secondary())
        expr_code.clear_secondary()

        self.__env["variables"][variable.getText()] = expr_name

        code = self.__code_creator.set_variable_value(
            env=self.__env["var"], name=f'"{variable.getText()}"', value=expr_name
        )

        return "", wrap_codes([code, expr_code])  # TODO

    def visitAssignment(self, ctx: LispParser.AssignmentContext) -> VisitResult:
        # TODO: копипаста

        variable = ctx.variable().getText()
        expression = ctx.expression()

        if not self.__has_variable(self.__env, variable):
            raise VisitingException(
                message=f'Unexpected variable "{variable}"', ctx=ctx
            )

        expr_name, expr_code = self.visit(expression)
        self.__env["code"].add_secondary_prolog(expr_code.render_secondary())
        expr_code.clear_secondary()

        self.__update_variable(env=self.__env, name=variable, new_value=expr_name)

        assignment_name = self.__variable_manager.create_object_name()

        assignment_code = self.__code_creator.update_variable_value(
            var=assignment_name,
            env=self.__env["var"],
            name=f'"{variable}"',
            value=expr_name,
        )

        return assignment_name, wrap_codes([assignment_code, expr_code])

    def visitLet(self, ctx: LispParser.LetContext):

        old_env = self.__env

        env_name = self.__variable_manager.create_environment_name()

        code = self.__code_creator.make_environment(
            var=env_name, parentEnv=old_env["var"]
        )

        new_env = {"prev": old_env, "var": env_name, "variables": {}, "code": code}

        self.__env = new_env

        binding_list = ctx.bindingList()

        codes = [r[1] for r in self.visit(binding_list)]

        code.update_data(varCount=len(codes))

        body_name, body_code_text = self.visitBody(ctx.body())

        code.add_main_epilog(
            join_codes(codes).replace("\n\n", "\n") + "\n" + body_code_text + "\n"
        )
        code.add_secondary_prolog("\n")

        self.__env = old_env

        return body_name, code

    def visitBindingList(self, ctx: LispParser.BindingListContext) -> list[VisitResult]:
        return [self.visit(b) for b in ctx.binding()]

    def visitBinding(self, ctx: LispParser.BindingContext):
        variable = ctx.variable()

        expression = ctx.expression()
        expr_name, expr_code = self.visit(expression)

        self.__env["code"].add_secondary_prolog(expr_code.render_secondary())
        expr_code.clear_secondary()

        if self.__env["variables"].get(variable.getText(), None):
            raise VisitingException(
                f'Variable "{variable.getText()}" appeared more than once in the bindings',
                ctx=ctx,
            )

        self.__env["variables"][variable.getText()] = expr_name

        code = self.__code_creator.set_variable_value(
            env=self.__env["var"], name=f'"{variable.getText()}"', value=expr_name
        )

        return "", wrap_codes([code, expr_code])  # TODO

    def visitBody(self, ctx: LispParser.BodyContext) -> tuple[str, str]:
        expressions = ctx.expression()

        expressions_names = []
        expression_codes = []

        for e in expressions:
            e_name, e_code = self.visit(e)
            self.__env["code"].add_secondary_prolog(e_code.render_secondary())
            e_code.clear_secondary()

            expressions_names.append(e_name)
            expression_codes.append(e_code)

        return expressions_names[-1], join_codes(expression_codes)

    def visitVariable(self, ctx: LispParser.VariableContext) -> VisitResult:
        variable = ctx.getText()

        # TODO: handle situation when variable is a standard-library function (like '+')

        if not self.__has_variable(self.__env, variable):
            raise VisitingException(
                message=f'Unexpected variable "{variable}"', ctx=ctx
            )

        expr_name = self.__variable_manager.create_object_name()
        expr_code = self.__code_creator.get_variable_value(
            var=expr_name, env=self.__env["var"], name=f'"{variable}"'
        )

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
        expr_var_name = self.__variable_manager.create_object_name()
        code.update_data(var=expr_var_name, value=value)

        return expr_var_name, code

    def __visit_function(
        self, function_name: str, operand_names: list[str], operand_codes: list[Code]
    ) -> VisitResult:
        if self.__condition_visiting_ctx.should_make_evaluable:
            expr_code = self.__code_creator.make_evaluable()
        else:
            expr_code = self.__code_creator.function_call()

        expr_var_name = self.__variable_manager.create_object_name()
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
