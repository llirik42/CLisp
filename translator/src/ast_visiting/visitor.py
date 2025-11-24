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
from src.environment import EnvironmentContext
from src.evaluable_context import EvaluableContext
from src.lambda_context import LambdaContext
from src.symbols import Symbols
from src.variable_manager import VariableManager
from .exceptions import (
    UnexpectedIdentifierException,
    FunctionRedefineException,
    UnknownFunctionException,
    DuplicatedBindingException,
    DuplicatedParamException,
    ParamNameConflictException,
)
from ..code_rendering.codes import MakePrimitiveCode

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
        symbols: Symbols,
        code_creator: CodeCreator,
        variable_manager: VariableManager,
        evaluable_context: EvaluableContext,
        environment_context: EnvironmentContext,
        lambda_context: LambdaContext,
    ):
        """
        Class represents a visitor of AST of the Lisp. Result of the visiting - code on C, that can be used in interpretation.

        :param symbols: standard elements.
        :param code_creator: code creator.
        :param variable_manager: variable manager.
        :param evaluable_context: evaluable context.
        :param environment_context: environment context.
        """

        self.__symbols = symbols
        self.__code_creator = code_creator
        self.__variable_manager = variable_manager
        self.__evaluable_ctx = evaluable_context
        self.__environment_ctx = environment_context
        self.__lambda_ctx = lambda_context
        self.__function_definitions = []

    def visitProgram(self, ctx: LispParser.ProgramContext) -> ProgramVisitResult:
        global_env_creation_func = "create_global_env"

        global_env_name = self.__variable_manager.create_environment_name()
        main_code = self.__code_creator.get_global_environment()
        main_code.update_data(
            var=global_env_name,
            get_func=global_env_creation_func,
        )

        # Обход выражений программы
        with self.__environment_ctx:
            self.__environment_ctx.init(code=main_code, name=global_env_name)
            elements_codes = [self.visit(e)[1] for e in ctx.programElement()]
        for c in elements_codes:
            c.make_final()
        if len(elements_codes) != 0:
            main_code.add_main_epilog(f"\n{join_codes(elements_codes)}")

        self.__variable_manager.reset_object_count()

        program_code = self.__code_creator.program()
        program_code.update_data(
            declarations=[c.render() for c in self.__function_definitions],
            main_body=main_code.render(),
        )

        return program_code.render()

    def visitDefinition(
        self, ctx: LispParser.DefinitionContext
    ) -> ExpressionVisitResult:
        # TODO: change when addint internal definitions (in let and in body of lambda)

        variable_name = ctx.variable().getText()
        if self.__symbols.has_api_symbol(variable_name):
            raise FunctionRedefineException(variable_name, ctx)

        expression = ctx.expression()
        expr_name, expr_code = self.visit(expression)

        expr_code.remove_first_secondary_line()
        self.__environment_ctx.update_variable(variable_name, expr_name)

        definition_code = self.__code_creator.set_variable_value()
        definition_code.update_data(
            env=self.__environment_ctx.name,
            name=f'"{variable_name}"',
            value=expr_name,
        )

        # First element is ignored and needed to unify the processing of expressions and definitions
        return "", wrap_codes(definition_code, expr_code)

    def visitAssignment(
        self, ctx: LispParser.AssignmentContext
    ) -> ExpressionVisitResult:
        # TODO: обработать ситуацию, когда меняется аргумент функции

        variable_name = ctx.variable().getText()

        if self.__lambda_ctx.inside_lambda:
            env = self.__lambda_ctx.environment
            env_name = "env"  # TODO: прибито

            if variable_name in self.__lambda_ctx.params:
                # TODO
                pass
        else:
            env = self.__environment_ctx.env
            env_name = self.__environment_ctx.name

        if not env.has_variable_recursively(variable_name):
            raise UnexpectedIdentifierException(variable_name, ctx)

        expression = ctx.expression()
        expr_name, expr_code = self.visit(expression)

        expr_code.remove_first_secondary_line()
        self.__environment_ctx.update_variable_recursively(variable_name, expr_name)

        assignment_name = self.__variable_manager.create_object_name()
        assignment_code = self.__code_creator.update_variable_value()
        assignment_code.update_data(
            var=assignment_name,
            env=env_name,
            name=f'"{variable_name}"',
            value=expr_name,
        )

        return assignment_name, wrap_codes(assignment_code, expr_code)

    def visitLet(self, ctx: LispParser.LetContext) -> ExpressionVisitResult:
        new_env_name = self.__variable_manager.create_environment_name()
        new_env_code = self.__code_creator.make_environment()
        new_env_code.update_data(var=new_env_name, parent=self.__environment_ctx.name)

        binding_list = ctx.bindingList()

        with self.__environment_ctx:
            self.__environment_ctx.init(code=new_env_code, name=new_env_name)

            bindings_codes = [c for c in self.visit(binding_list)]
            body_name, body_code = self.visit(ctx.environmentBody())

            joined_bindings_codes = join_codes(bindings_codes).replace("\n\n", "\n")
            new_env_code.add_main_epilog(f"{joined_bindings_codes}\n{body_code}")

        return body_name, new_env_code

    def visitBindingList(
        self, ctx: LispParser.BindingListContext
    ) -> list[BindingVisitResult]:
        return [self.visit(b) for b in ctx.binding()]

    def visitBinding(self, ctx: LispParser.BindingContext) -> BindingVisitResult:
        variable_name = ctx.variable().getText()

        if self.__symbols.has_api_symbol(variable_name):
            raise FunctionRedefineException(variable_name, ctx)

        if self.__environment_ctx.has_variable(variable_name):
            raise DuplicatedBindingException(variable_name, ctx)

        expression = ctx.expression()
        expr_name, expr_code = self.visit(expression)
        expr_code.remove_first_secondary_line()
        self.__environment_ctx.update_variable(variable_name, expr_name)

        binding_code = self.__code_creator.set_variable_value()
        binding_code.update_data(
            env=self.__environment_ctx.name,
            name=f'"{variable_name}"',
            value=expr_name,
        )

        return wrap_codes(binding_code, expr_code)

    def visitProcedureBody(
        self, ctx: LispParser.ProcedureBodyContext
    ) -> BodyVisitResult:
        # TODO: visit definitions

        expressions = ctx.expression()

        expr_names = []
        expr_codes = []

        for i, e in enumerate(expressions):
            e_name, e_code = self.visit(e)

            # TODO: fix
            if i == len(expressions) - 1:
                e_code.remove_first_secondary_line()

            e_code.make_final()
            expr_names.append(e_name)
            expr_codes.append(e_code)

        return expr_names[-1], join_codes(expr_codes)

    def visitEnvironmentBody(
        self, ctx: LispParser.EnvironmentBodyContext
    ) -> BodyVisitResult:
        # TODO: visit internal definitions

        expressions = ctx.expression()

        expr_names = []
        expr_codes = []

        for e in expressions:
            e_name, e_code = self.visit(e)
            transfer_secondary(e_code, self.__environment_ctx.code)

            expr_names.append(e_name)
            expr_codes.append(e_code)

        return expr_names[-1], join_codes(expr_codes)

    def visitVariable(self, ctx: LispParser.VariableContext) -> ExpressionVisitResult:
        # TODO: correctly handle the situation when variable is a function (like '+')

        variable_name = ctx.getText()

        # TODO: корректно обрабатывать ситуацию, когда переменной нет в сигнатуре лямбды
        if (
            self.__lambda_ctx.inside_lambda
            and variable_name in self.__lambda_ctx.params
        ):
            param_name = self.__lambda_ctx.get_param_c_name(variable_name)[
                0
            ]  # TODO: использовать не кортеж

            return param_name, self.__code_creator.empty()

        if not self.__environment_ctx.has_variable_recursively(variable_name):
            raise UnexpectedIdentifierException(variable_name, ctx)

        expr_name = self.__variable_manager.create_object_name()
        expr_code = self.__code_creator.get_variable_value()
        expr_code.update_data(
            var=expr_name, env=self.__environment_ctx.name, name=f'"{variable_name}"'
        )

        return expr_name, expr_code

    def visitCondition(self, ctx: LispParser.ConditionContext) -> ExpressionVisitResult:
        symbol = "if"
        c_name = self.__symbols.find_api_symbol(symbol)
        assert c_name is not None, f'Symbol "{symbol}" is not found'

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
            function_name=c_name,
            operand_names=operand_names,
            operand_codes=operand_codes,
        )

    def visitAnd(self, ctx: LispParser.AndContext) -> ExpressionVisitResult:
        symbol = "and"
        c_name = self.__symbols.find_api_symbol(symbol)
        assert c_name is not None, f'Symbol "{symbol}" is not found'

        with self.__evaluable_ctx:
            operand_names, operand_codes = self.__visit_operands(ctx.test())

        return self.__visit_function(
            function_name=c_name,
            operand_names=operand_names,
            operand_codes=operand_codes,
        )

    def visitOr(self, ctx: LispParser.OrContext) -> ExpressionVisitResult:
        symbol = "or"
        c_name = self.__symbols.find_api_symbol(symbol)
        assert c_name is not None, f'Symbol "{symbol}" is not found'

        with self.__evaluable_ctx:
            operand_names, operand_codes = self.__visit_operands(ctx.test())

        return self.__visit_function(
            function_name=c_name,
            operand_names=operand_names,
            operand_codes=operand_codes,
        )

    def visitProcedureCall(
        self, ctx: LispParser.ProcedureCallContext
    ) -> ExpressionVisitResult:
        # TODO: add support of calling lambdas

        lisp_function = ctx.operator().getText()

        c_name = self.__symbols.find_api_symbol(lisp_function)
        if c_name is None:
            raise UnknownFunctionException(lisp_function, ctx)

        operand_names, operand_codes = self.__visit_operands(ctx.operand())

        return self.__visit_function(
            function_name=c_name,
            operand_names=operand_names,
            operand_codes=operand_codes,
        )

    def visitProcedure(self, ctx: LispParser.ProcedureContext) -> ExpressionVisitResult:
        procedure_env_name = "env"  # TODO: прибито (из шаблона)

        # TODO: Нужно проверять количество аргументов, переданных в лямбду при компиляции

        formals = ctx.formals()
        body = ctx.procedureBody()

        function_code = self.__code_creator.lambda_definition()

        with self.__lambda_ctx, self.__environment_ctx:
            self.__environment_ctx.init(
                name=procedure_env_name, code=self.__environment_ctx.code
            )

            self.__lambda_ctx.set_environment(self.__environment_ctx.env)

            formals_text_before, formals_text_after = self.visitFormals(formals)
            body_name, body_code_text = self.visit(body)

        function_name = self.__variable_manager.create_function_name()

        if formals_text_before:
            body = formals_text_before + "\n\n"
        else:
            body = ""

        if body_code_text == "":
            body += formals_text_after
        else:
            body += body_code_text + formals_text_after

        function_code.update_data(
            func=function_name,
            ret_var=body_name,
            body=body,
        )

        self.__function_definitions.append(function_code)
        function_code.make_final()

        lambda_variable = self.__variable_manager.create_object_name()
        lambda_creation_code = self.__code_creator.make_lambda()
        lambda_creation_code.update_data(
            var=lambda_variable, func=function_name, env=self.__environment_ctx.name
        )

        return lambda_variable, lambda_creation_code

    def visitFixedFormals(self, ctx: LispParser.FixedFormalsContext) -> tuple[str, str]:
        variables = ctx.variable()

        codes = []
        lisp_names = []
        for i, v in enumerate(variables):
            param_lisp_name = v.getText()
            if param_lisp_name in lisp_names:
                raise DuplicatedParamException(param_lisp_name, ctx)
            if self.__symbols.has_api_symbol(param_lisp_name):
                raise ParamNameConflictException(param_lisp_name, ctx)
            lisp_names.append(param_lisp_name)

            param_c_name = self.__variable_manager.create_object_name()
            current_arg_getting_code = self.__code_creator.get_function_argument()
            current_arg_getting_code.update_data(index=i, var=param_c_name)

            current_arg_getting_code.make_final_final()
            codes.append(current_arg_getting_code)
            self.__lambda_ctx.add_param(
                lisp_name=param_lisp_name, c_name=param_c_name, variadic=False
            )

        return join_codes(codes), ""

    def visitListFormals(self, ctx: LispParser.ListFormalsContext) -> tuple[str, str]:
        count = "count"
        args = "args"

        param_lisp_name = ctx.variable().getText()
        if self.__symbols.has_api_symbol(param_lisp_name):
            raise ParamNameConflictException(param_lisp_name, ctx)

        arg_c_name = self.__variable_manager.create_object_name()
        arg_getting_code = self.__code_creator.make_list()
        arg_getting_code.update_data(var=arg_c_name, count=count, elements=args)

        arg_getting_code.make_final_final()

        secondary = arg_getting_code.render_secondary() + "\n"
        arg_getting_code.clear_secondary()

        self.__lambda_ctx.add_param(
            lisp_name=param_lisp_name, c_name=arg_c_name, variadic=True
        )

        return arg_getting_code.render(), secondary

    def visitVariadicFormals(
        self, ctx: LispParser.VariadicFormalsContext
    ) -> tuple[str, str]:
        count = "count"
        args = "args"

        fixed_variables = ctx.variable()[:-1]
        variadic_variable = ctx.variable()[-1]

        codes_to_join = []
        lisp_names = []

        for i, v in enumerate(fixed_variables):
            param_lisp_name = v.getText()
            if param_lisp_name in lisp_names:
                raise DuplicatedParamException(param_lisp_name, ctx)
            if self.__symbols.has_api_symbol(param_lisp_name):
                raise ParamNameConflictException(param_lisp_name, ctx)
            lisp_names.append(param_lisp_name)

            current_arg_c_name = self.__variable_manager.create_object_name()
            current_arg_getting_code = self.__code_creator.get_function_argument()
            current_arg_getting_code.update_data(index=i, var=current_arg_c_name)

            current_arg_getting_code.make_final_final()
            codes_to_join.append(current_arg_getting_code)
            self.__lambda_ctx.add_param(
                lisp_name=param_lisp_name, c_name=current_arg_c_name, variadic=False
            )

        # Variadic
        variadic_lisp_name = variadic_variable.getText()
        if variadic_lisp_name in lisp_names:
            raise DuplicatedParamException(variadic_lisp_name, ctx)
        if self.__symbols.has_api_symbol(variadic_lisp_name):
            raise ParamNameConflictException(variadic_lisp_name, ctx)

        variadic_arg_c_name = self.__variable_manager.create_object_name()
        variadic_arg_getting_code = self.__code_creator.make_list()
        variadic_arg_getting_code.update_data(
            var=variadic_arg_c_name,
            count=f"{count}-{len(fixed_variables)}",
            elements=f"{args}+{len(fixed_variables)}",
        )

        variadic_arg_getting_code.make_final_final()

        secondary = variadic_arg_getting_code.render_secondary() + "\n"
        variadic_arg_getting_code.clear_secondary()
        codes_to_join.append(variadic_arg_getting_code)

        self.__lambda_ctx.add_param(
            lisp_name=variadic_lisp_name,
            c_name=variadic_arg_c_name,
            variadic=True,
        )

        return join_codes(codes_to_join), secondary

    def visitBoolConstant(
        self, ctx: LispParser.BoolConstantContext
    ) -> ExpressionVisitResult:
        code = self.__code_creator.make_boolean()
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

        code = self.__code_creator.make_character()

        return self.__visit_constant(code=code, value=f"'{value}'")

    def visitStringConstant(
        self, ctx: LispParser.StringConstantContext
    ) -> ExpressionVisitResult:
        code = self.__code_creator.make_string()

        return self.__visit_constant(code=code, value=ctx.getText())

    def visitIntegerConstant(
        self, ctx: LispParser.IntegerConstantContext
    ) -> ExpressionVisitResult:
        code = self.__code_creator.make_int()

        return self.__visit_constant(code=code, value=int(ctx.getText()))

    def visitFloatConstant(
        self, ctx: LispParser.FloatConstantContext
    ) -> ExpressionVisitResult:
        code = self.__code_creator.make_float()

        return self.__visit_constant(code=code, value=float(ctx.getText()))

    def __visit_constant(
        self, code: MakePrimitiveCode, value: Union[str, int, float]
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
            expr_code = self.__code_creator.procedure_call()

        expr_var_name = self.__variable_manager.create_object_name()
        expr_code.update_data(func=function_name, args=operand_names, var=expr_var_name)
        wrapped_expr_code = wrap_codes(expr_code, operand_codes)

        return expr_var_name, wrapped_expr_code

    def __visit_operands(self, operands) -> tuple[list[str], list[Code]]:
        operand_names = []
        operand_codes = []

        for op in operands:
            op_name, op_template = self.visit(op)
            operand_names.append(op_name)
            operand_codes.append(op_template)

        return operand_names, operand_codes
