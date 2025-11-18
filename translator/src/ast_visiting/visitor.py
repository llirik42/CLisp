from typing import Union

from src.LispParser import LispParser
from src.LispVisitor import LispVisitor
from src.code_rendering import CodeCreator, Code, wrap_codes, join_codes, transfer_secondary
from src.function_table import FunctionTable
from src.variable_manager import VariableManager
from .environment import EnvironmentContext
from .evaluable_context import EvaluableContext
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
        self.__evaluable_ctx = EvaluableContext()
        self.__environment_ctx = EnvironmentContext()

    def visitProgram(self, ctx: LispParser.ProgramContext) -> str:
        global_env_var_name = self.__variable_manager.create_environment_name()

        global_env_code = self.__code_creator.make_environment(
            var=global_env_var_name, parentEnv="NULL"
        )

        with self.__environment_ctx:
            self.__environment_ctx.init(code=global_env_code, name=global_env_var_name)
            
            codes = [self.visit(e)[1] for e in ctx.programElement()]

            global_env_code.update_data(varCount=self.__environment_ctx.variable_count)

        for c in codes:
            c.make_final()

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

        transfer_secondary(expr_code, self.__environment_ctx.code)

        self.__environment_ctx.update_variable(variable.getText(), expr_name)

        code = self.__code_creator.set_variable_value(
            env=self.__environment_ctx.name, name=f'"{variable.getText()}"', value=expr_name
        )

        return "", wrap_codes([code, expr_code])  # TODO

    def visitAssignment(self, ctx: LispParser.AssignmentContext) -> VisitResult:
        # TODO: копипаста

        variable = ctx.variable().getText()
        expression = ctx.expression()

        if not self.__environment_ctx.has_variable_recursively(variable):
            raise VisitingException(
                message=f'Unexpected variable "{variable}"', ctx=ctx
            )

        expr_name, expr_code = self.visit(expression)

        transfer_secondary(expr_code, self.__environment_ctx.code)

        self.__environment_ctx.update_variable_recursively(variable, expr_name)

        assignment_name = self.__variable_manager.create_object_name()

        assignment_code = self.__code_creator.update_variable_value(
            var=assignment_name,
            env=self.__environment_ctx.name,
            name=f'"{variable}"',
            value=expr_name,
        )

        return assignment_name, wrap_codes([assignment_code, expr_code])

    def visitLet(self, ctx: LispParser.LetContext):
        new_env_name = self.__variable_manager.create_environment_name()

        new_env_code = self.__code_creator.make_environment(
            var=new_env_name, parentEnv=self.__environment_ctx.name
        )

        binding_list = ctx.bindingList()

        with self.__environment_ctx:
            self.__environment_ctx.init(code=new_env_code, name=new_env_name)
            codes = [r[1] for r in self.visit(binding_list)]
            body_name, body_code_text = self.visitBody(ctx.body())

            code = self.__environment_ctx.code
            code.update_data(varCount=len(codes))
            code.add_main_epilog(
                join_codes(codes).replace("\n\n", "\n") + "\n" + body_code_text + "\n"
            )
            code.add_secondary_prolog("\n")

        return body_name, new_env_code

    def visitBindingList(self, ctx: LispParser.BindingListContext) -> list[VisitResult]:
        return [self.visit(b) for b in ctx.binding()]

    def visitBinding(self, ctx: LispParser.BindingContext):
        variable = ctx.variable()

        expression = ctx.expression()
        expr_name, expr_code = self.visit(expression)

        transfer_secondary(expr_code, self.__environment_ctx.code)

        if self.__environment_ctx.has_variable(variable.getText()):
            raise VisitingException(
                f'Variable "{variable.getText()}" appeared more than once in the bindings',
                ctx=ctx,
            )

        self.__environment_ctx.update_variable(variable.getText(), expr_name)

        code = self.__code_creator.set_variable_value(
            env=self.__environment_ctx.name, name=f'"{variable.getText()}"', value=expr_name
        )

        return "", wrap_codes([code, expr_code])  # TODO

    def visitBody(self, ctx: LispParser.BodyContext) -> tuple[str, str]:
        expressions = ctx.expression()

        expressions_names = []
        expression_codes = []

        for e in expressions:
            e_name, e_code = self.visit(e)
            transfer_secondary(e_code, self.__environment_ctx.code)

            expressions_names.append(e_name)
            expression_codes.append(e_code)

        return expressions_names[-1], join_codes(expression_codes)

    def visitVariable(self, ctx: LispParser.VariableContext) -> VisitResult:
        variable = ctx.getText()

        # TODO: handle situation when variable is a standard-library function (like '+')

        if not self.__environment_ctx.has_variable_recursively(variable):
            raise VisitingException(
                message=f'Unexpected variable "{variable}"', ctx=ctx
            )

        expr_name = self.__variable_manager.create_object_name()
        expr_code = self.__code_creator.get_variable_value(
            var=expr_name, env=self.__environment_ctx.name, name=f'"{variable}"'
        )

        return expr_name, expr_code

    def visitCondition(self, ctx: LispParser.ConditionContext) -> VisitResult:
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

    def visitAnd(self, ctx: LispParser.AndContext) -> VisitResult:
        identifier = "and"
        c_function = self.__function_table.get_c_func(identifier)

        with self.__evaluable_ctx:
            operand_names, operand_codes = self.__visit_operands(ctx.test())

        return self.__visit_function(
            function_name=c_function,
            operand_names=operand_names,
            operand_codes=operand_codes,
        )

    def visitOr(self, ctx: LispParser.OrContext) -> VisitResult:
        identifier = "or"
        c_function = self.__function_table.get_c_func(identifier)

        with self.__evaluable_ctx:
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
