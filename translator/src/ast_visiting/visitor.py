from typing import Union

from src.LispParser import LispParser
from src.LispVisitor import LispVisitor
from src.code_rendering import (
    CodeCreator,
    Code,
    wrap_codes,
    join_codes,
    transfer_secondary,
)
from src.function_table import FunctionTable
from src.variable_manager import VariableManager
from .exceptions import VisitingException

from src.evaluable_context import EvaluableContext
from src.environment import EnvironmentContext

# TODO
# (variable, code)
ExpressionVisitResult = tuple[str, Code]

# (variable that matches the last expression, code)
BodyVisitResult = tuple[str, str]

# code of creating value of the variable and binding it
BindingVisitResult = Code

# text of the output C-program
ProgramVisitResult = str


class ASTVisitor(LispVisitor):
    def __init__(
        self,
        function_table: FunctionTable,
        code_creator: CodeCreator,
        variable_manager: VariableManager,
        evaluable_context: EvaluableContext,
        environment_context: EnvironmentContext,
    ):
        """
        Class represents a visitor of AST of the Lisp. Result of the visiting - code on C, that can be used in interpretation.

        :param function_table: function table.
        :param code_creator: code creator.
        :param variable_manager: variable manager.
        :param evaluable_context: evaluable context.
        :param environment_context: environment context.
        """

        self.__function_table = function_table
        self.__code_creator = code_creator
        self.__variable_manager = variable_manager
        self.__evaluable_ctx = evaluable_context
        self.__environment_ctx = environment_context

    def visitProgram(self, ctx: LispParser.ProgramContext) -> ProgramVisitResult:
        top_level_env_name = self.__variable_manager.create_environment_name()
        top_level_env_code = self.__code_creator.make_environment(
            var=top_level_env_name
        )

        with self.__environment_ctx:
            self.__environment_ctx.init(
                code=top_level_env_code, name=top_level_env_name
            )

            elements_codes = [self.visit(e)[1] for e in ctx.programElement()]
            top_level_env_code.update_data(
                varCount=self.__environment_ctx.variable_count
            )

        for c in elements_codes:
            c.make_final()

        top_level_env_code.add_main_epilog(f"\n{join_codes(elements_codes)}")

        main_function_code = self.__code_creator.main_function(
            code=f"{top_level_env_code.render()}\n"
        )

        return main_function_code.render()

    def visitDefinition(
        self, ctx: LispParser.DefinitionContext
    ) -> ExpressionVisitResult:
        variable_name = ctx.variable().getText()
        if self.__function_table.has_identifier(variable_name):
            raise VisitingException(
                f'The standard library function "{variable_name}" cannot be redefined!',
                ctx,
            )

        expression = ctx.expression()
        expr_name, expr_code = self.visit(expression)

        transfer_secondary(expr_code, self.__environment_ctx.code)
        self.__environment_ctx.update_variable(variable_name, expr_name)

        code = self.__code_creator.set_variable_value(
            env=self.__environment_ctx.name,
            name=f'"{variable_name}"',
            value=expr_name,
        )

        # First element is ignored and needed to unify the processing of expressions and definitions
        return "", wrap_codes([code, expr_code])

    def visitAssignment(
        self, ctx: LispParser.AssignmentContext
    ) -> ExpressionVisitResult:
        variable_name = ctx.variable().getText()

        if not self.__environment_ctx.has_variable_recursively(variable_name):
            raise VisitingException(
                message=f'Unexpected variable "{variable_name}"', ctx=ctx
            )

        expression = ctx.expression()
        expr_name, expr_code = self.visit(expression)

        transfer_secondary(expr_code, self.__environment_ctx.code)
        self.__environment_ctx.update_variable_recursively(variable_name, expr_name)

        assignment_name = self.__variable_manager.create_object_name()
        assignment_code = self.__code_creator.update_variable_value(
            var=assignment_name,
            env=self.__environment_ctx.name,
            name=f'"{variable_name}"',
            value=expr_name,
        )

        return assignment_name, wrap_codes([assignment_code, expr_code])

    def visitLet(self, ctx: LispParser.LetContext) -> ExpressionVisitResult:
        new_env_name = self.__variable_manager.create_environment_name()
        new_env_code = self.__code_creator.make_environment(
            var=new_env_name, parentEnv=self.__environment_ctx.name
        )

        binding_list = ctx.bindingList()

        with self.__environment_ctx:
            self.__environment_ctx.init(code=new_env_code, name=new_env_name)

            bindings_codes = [c for c in self.visit(binding_list)]
            body_name, body_code = self.visitBody(ctx.body())

            # TODO: add internal definitions to varCount
            new_env_code.update_data(varCount=len(bindings_codes))

            joined_bindings_codes = join_codes(bindings_codes).replace("\n\n", "\n")
            new_env_code.add_main_epilog(f"{joined_bindings_codes}\n{body_code}\n")
            new_env_code.add_secondary_prolog("\n")

        return body_name, new_env_code

    def visitBindingList(
        self, ctx: LispParser.BindingListContext
    ) -> list[BindingVisitResult]:
        return [self.visit(b) for b in ctx.binding()]

    def visitBinding(self, ctx: LispParser.BindingContext) -> BindingVisitResult:
        variable_name = ctx.variable().getText()

        if self.__function_table.has_identifier(variable_name):
            raise VisitingException(
                f'The standard library function "{variable_name}" cannot be redefined!',
                ctx,
            )

        if self.__environment_ctx.has_variable(variable_name):
            raise VisitingException(
                f'Variable "{variable_name}" appeared more than once in the bindings',
                ctx=ctx,
            )

        expression = ctx.expression()
        expr_name, expr_code = self.visit(expression)
        transfer_secondary(expr_code, self.__environment_ctx.code)
        self.__environment_ctx.update_variable(variable_name, expr_name)

        binding_code = self.__code_creator.set_variable_value(
            env=self.__environment_ctx.name,
            name=f'"{variable_name}"',
            value=expr_name,
        )

        return wrap_codes([binding_code, expr_code])

    def visitBody(self, ctx: LispParser.BodyContext) -> BodyVisitResult:
        expressions = ctx.expression()

        expr_names = []
        expr_codes = []

        for e in expressions:
            # TODO: change for body of lambda
            e_name, e_code = self.visit(e)
            transfer_secondary(e_code, self.__environment_ctx.code)

            expr_names.append(e_name)
            expr_codes.append(e_code)

        return expr_names[-1], join_codes(expr_codes)

    def visitVariable(self, ctx: LispParser.VariableContext) -> ExpressionVisitResult:
        # TODO: correctly handle the situation when variable is a function (like '+')

        variable_name = ctx.getText()

        if not self.__environment_ctx.has_variable_recursively(variable_name):
            raise VisitingException(
                message=f'Unexpected variable "{variable_name}"', ctx=ctx
            )

        expr_name = self.__variable_manager.create_object_name()
        expr_code = self.__code_creator.get_variable_value(
            var=expr_name, env=self.__environment_ctx.name, name=f'"{variable_name}"'
        )

        return expr_name, expr_code

    def visitCondition(self, ctx: LispParser.ConditionContext) -> ExpressionVisitResult:
        identifier = "if"
        c_function = self.__function_table.get_c_func(identifier)

        test = ctx.test()
        consequent = ctx.consequent()
        alternate = ctx.alternate()

        test_name, test_code = self.visit(test)
        with self.__evaluable_ctx:
            consequent_name, consequent_code = self.visit(consequent)

        operand_names = [test_name, consequent_name]
        operand_codes = [test_code, consequent_code]

        if alternate is not None:
            with self.__evaluable_ctx:
                alternate_name, alternate_code = self.visit(alternate)
            operand_names.append(alternate_name)
            operand_codes.append(alternate_code)

        return self.__visit_function(
            function_name=c_function,
            operand_names=operand_names,
            operand_codes=operand_codes,
        )

    def visitAnd(self, ctx: LispParser.AndContext) -> ExpressionVisitResult:
        identifier = "and"
        c_function = self.__function_table.get_c_func(identifier)

        with self.__evaluable_ctx:
            operand_names, operand_codes = self.__visit_operands(ctx.test())

        return self.__visit_function(
            function_name=c_function,
            operand_names=operand_names,
            operand_codes=operand_codes,
        )

    def visitOr(self, ctx: LispParser.OrContext) -> ExpressionVisitResult:
        identifier = "or"
        c_function = self.__function_table.get_c_func(identifier)

        with self.__evaluable_ctx:
            operand_names, operand_codes = self.__visit_operands(ctx.test())

        return self.__visit_function(
            function_name=c_function,
            operand_names=operand_names,
            operand_codes=operand_codes,
        )

    def visitProcedureCall(
        self, ctx: LispParser.ProcedureCallContext
    ) -> ExpressionVisitResult:
        # TODO: add support of calling lambdas

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

    def visitBoolConstant(
        self, ctx: LispParser.BoolConstantContext
    ) -> ExpressionVisitResult:
        c_function = self.__function_table.get_c_func("#boolean#")

        code = self.__code_creator.make_constant(function=c_function)
        value = 1 if ctx.getText() == "#t" else 0

        return self.__visit_constant(
            code=code,
            value=value,
        )

    def visitCharacterConstant(
        self, ctx: LispParser.CharacterConstantContext
    ) -> ExpressionVisitResult:
        value = f"{ctx.getText()[2:]}"

        if value == "'":
            value = "\\'"  # Escape single quote

        c_function = self.__function_table.get_c_func("#character#")
        code = self.__code_creator.make_constant(function=c_function)

        return self.__visit_constant(code=code, value=f"'{value}'")

    def visitStringConstant(
        self, ctx: LispParser.StringConstantContext
    ) -> ExpressionVisitResult:
        c_function = self.__function_table.get_c_func("#string#")
        code = self.__code_creator.make_constant(function=c_function)

        return self.__visit_constant(code=code, value=ctx.getText())

    def visitIntegerConstant(
        self, ctx: LispParser.IntegerConstantContext
    ) -> ExpressionVisitResult:
        c_function = self.__function_table.get_c_func("#integer#")
        code = self.__code_creator.make_constant(function=c_function)

        return self.__visit_constant(code=code, value=int(ctx.getText()))

    def visitFloatConstant(
        self, ctx: LispParser.FloatConstantContext
    ) -> ExpressionVisitResult:
        c_function = self.__function_table.get_c_func("#float#")
        code = self.__code_creator.make_constant(function=c_function)

        return self.__visit_constant(code=code, value=float(ctx.getText()))

    def __visit_constant(
        self, code: Code, value: Union[str, int, float]
    ) -> ExpressionVisitResult:
        expr_var_name = self.__variable_manager.create_object_name()
        code.update_data(var=expr_var_name, value=value)

        return expr_var_name, code

    def __visit_function(
        self, function_name: str, operand_names: list[str], operand_codes: list[Code]
    ) -> ExpressionVisitResult:
        if self.__evaluable_ctx.should_make_evaluable:
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
