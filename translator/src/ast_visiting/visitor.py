from typing import Union

from src.LispParser import LispParser
from src.LispVisitor import LispVisitor
from src.rendering import (
    CodeCreator,
    wrap_codes,
    join_codes,
    transfer_secondary,
)
from .declarations_context import DeclarationsContext
from .environment_context import EnvironmentContext
from .evaluable_context import EvaluableContext
from .lambda_context import LambdaContext
from src.symbols import Symbols
from .variable_manager import VariableManager
from .exceptions import (
    UnexpectedIdentifierException,
    FunctionRedefineException,
    DuplicatedBindingException,
    DuplicatedParamException,
    ParamNameConflictException,
)
from src.rendering.codes import MakePrimitiveCode, Code

# (variable, code)
ExpressionVisitResult = tuple[str, Code]

# (variable that matches the last expression, code)
BodyVisitResult = tuple[str, str]

# code of creating value of the variable and binding it
BindingVisitResult = Code

# text of the output C-program
ProgramVisitResult = str


class ASTVisitor(LispVisitor):
    def __init__(self, symbols: Symbols, code_creator: CodeCreator):
        """
        Class represents a visitor of AST of the Lisp. Result of the visiting - code on C, that can be used in interpretation.

        :param symbols: standard elements.
        :param code_creator: code creator.
        :param symbols: symbols.
        :param code_creator: code creator.
        """

        self.__symbols = symbols
        self.__code_creator = code_creator
        self.__variable_manager = VariableManager()
        self.__evaluable_ctx = EvaluableContext()
        self.__environment_ctx = EnvironmentContext()
        self.__lambda_ctx = LambdaContext()
        self.__declaration_ctx = DeclarationsContext()

    def visitProgram(self, ctx: LispParser.ProgramContext) -> ProgramVisitResult:
        global_env_var = self.__variable_manager.create_environment_name()
        main_code = self.__code_creator.get_global_environment()
        main_code.update_data(var=global_env_var)

        # Обход выражений программы
        with self.__environment_ctx:
            self.__environment_ctx.init(code=main_code, name=global_env_var)
            env = self.__environment_ctx.env

            # Добавление функций стандартной библиотеки в глобальный контекст
            for lisp_name, _ in self.__symbols.find_api_function_items():
                env.add_variable(lisp_name)
            elements_codes = [self.visit(e)[1] for e in ctx.programElement()]
        for c in elements_codes:
            c.make_final()
        if len(elements_codes) != 0:
            main_code.add_main_epilog(f"\n{join_codes(elements_codes)}")

        program_code = self.__code_creator.program()

        program_code.update_data(
            declarations=[
                c.render() for c in self.__declaration_ctx.iter_declarations()
            ],
            main_body=main_code.render(),
        )

        return program_code.render()

    def visitDefinition(
        self, ctx: LispParser.DefinitionContext
    ) -> ExpressionVisitResult:
        env = self.__environment_ctx.env

        # TODO: change when addint internal definitions (in let and in body of lambda)

        variable_name = ctx.variable().getText()
        if self.__symbols.has_api_symbol(variable_name):
            raise FunctionRedefineException(variable_name, ctx)

        expression = ctx.expression()
        expr_var, expr_code = self.visit(expression)

        expr_code.remove_first_secondary_line()
        env.add_variable(variable_name)

        definition_code = self.__code_creator.set_variable_value()
        definition_code.update_data(
            env=env.name,
            name=f'"{variable_name}"',
            value=expr_var,
        )

        # First element is ignored and needed to unify the processing of expressions and definitions
        return "", wrap_codes(definition_code, expr_code)

    def visitAssignment(
        self, ctx: LispParser.AssignmentContext
    ) -> ExpressionVisitResult:
        # TODO: обработать ситуацию, когда меняется аргумент функции

        variable_name = ctx.variable().getText()

        if self.__lambda_ctx.inside_lambda and self.__lambda_ctx.has_param(
            variable_name
        ):
            # TODO: set! on lambda param
            raise RuntimeError("Not supported!")

        env = self.__environment_ctx.env

        if not env.has_variable_recursively(variable_name):
            raise UnexpectedIdentifierException(variable_name, ctx)

        expression = ctx.expression()
        expr_var, expr_code = self.visit(expression)

        expr_code.remove_first_secondary_line()

        assignment_var = self.__variable_manager.create_object_name()
        assignment_code = self.__code_creator.update_variable_value()
        assignment_code.update_data(
            var=assignment_var,
            env=env.name,
            name=f'"{variable_name}"',
            value=expr_var,
        )

        return assignment_var, wrap_codes(assignment_code, expr_code)

    def visitLet(self, ctx: LispParser.LetContext) -> ExpressionVisitResult:
        env = self.__environment_ctx.env

        new_env_var = self.__variable_manager.create_environment_name()
        new_env_code = self.__code_creator.make_environment()
        new_env_code.update_data(var=new_env_var, parent=env.name)

        binding_list = ctx.bindingList()

        with self.__environment_ctx:
            self.__environment_ctx.init(code=new_env_code, name=new_env_var)

            bindings_codes = [c for c in self.visit(binding_list)]
            body_var, body_code = self.visit(ctx.environmentBody())

            joined_bindings_codes = join_codes(bindings_codes).replace("\n\n", "\n")
            new_env_code.add_main_epilog(f"{joined_bindings_codes}\n{body_code}")

        return body_var, new_env_code

    def visitBindingList(
        self, ctx: LispParser.BindingListContext
    ) -> list[BindingVisitResult]:
        return [self.visit(b) for b in ctx.binding()]

    def visitBinding(self, ctx: LispParser.BindingContext) -> BindingVisitResult:
        env = self.__environment_ctx.env

        variable_name = ctx.variable().getText()

        if self.__symbols.has_api_symbol(variable_name):
            raise FunctionRedefineException(variable_name, ctx)

        if env.has_variable(variable_name):
            raise DuplicatedBindingException(variable_name, ctx)

        expression = ctx.expression()
        expr_var, expr_code = self.visit(expression)
        expr_code.remove_first_secondary_line()
        env.add_variable(variable_name)

        binding_code = self.__code_creator.set_variable_value()
        binding_code.update_data(
            env=env.name,
            name=f'"{variable_name}"',
            value=expr_var,
        )

        return wrap_codes(binding_code, expr_code)

    def visitProcedureBody(
        self, ctx: LispParser.ProcedureBodyContext
    ) -> BodyVisitResult:
        # TODO: visit definitions

        expressions = ctx.expression()

        expr_vars = []
        expr_codes = []

        for i, e in enumerate(expressions):
            e_var, e_code = self.visit(e)

            # TODO: fix
            if i == len(expressions) - 1:
                e_code.remove_first_secondary_line()

            e_code.make_final()
            expr_vars.append(e_var)
            expr_codes.append(e_code)

        return expr_vars[-1], join_codes(expr_codes)

    def visitEnvironmentBody(
        self, ctx: LispParser.EnvironmentBodyContext
    ) -> BodyVisitResult:
        # TODO: visit internal definitions

        env = self.__environment_ctx.env

        expressions = ctx.expression()

        expr_vars = []
        expr_codes = []

        for e in expressions:
            e_var, e_code = self.visit(e)
            transfer_secondary(e_code, env.code)

            expr_vars.append(e_var)
            expr_codes.append(e_code)

        return expr_vars[-1], join_codes(expr_codes)

    def visitVariable(self, ctx: LispParser.VariableContext) -> ExpressionVisitResult:
        variable_name = ctx.getText()

        if self.__lambda_ctx.inside_lambda and self.__lambda_ctx.has_param(
            variable_name
        ):
            param_var = self.__lambda_ctx.get_param_var(variable_name)
            empty_code = self.__code_creator.empty()
            return param_var, empty_code

        env = self.__environment_ctx.env

        if not env.has_variable_recursively(variable_name):
            raise UnexpectedIdentifierException(variable_name, ctx)

        expr_var = self.__variable_manager.create_object_name()
        expr_code = self.__code_creator.get_variable_value()
        expr_code.update_data(var=expr_var, env=env.name, name=f'"{variable_name}"')

        return expr_var, expr_code

    def visitCondition(self, ctx: LispParser.ConditionContext) -> ExpressionVisitResult:
        lisp_if = "if"
        c_name = self.__symbols.find_api_symbol(lisp_if)
        assert c_name is not None, f'Symbol "{lisp_if}" is not found'

        test = ctx.test()
        consequent = ctx.consequent()
        alternate = ctx.alternate()

        test_var, test_code = self.visit(test)
        with self.__evaluable_ctx:
            consequent_var, consequent_code = self.visit(consequent)

        operand_vars = [test_var, consequent_var]
        operand_codes = [test_code, consequent_code]

        if alternate is not None:
            with self.__evaluable_ctx:
                alternate_var, alternate_code = self.visit(alternate)
            operand_vars.append(alternate_var)
            operand_codes.append(alternate_code)

        return self.__visit_function(
            function_name=c_name,
            operand_names=operand_vars,
            operand_codes=operand_codes,
        )

    def visitAnd(self, ctx: LispParser.AndContext) -> ExpressionVisitResult:
        lisp_and = "and"
        c_name = self.__symbols.find_api_symbol(lisp_and)
        assert c_name is not None, f'Symbol "{lisp_and}" is not found'

        with self.__evaluable_ctx:
            operand_vars, operand_codes = self.__visit_operands(ctx.test())

        return self.__visit_function(
            function_name=c_name,
            operand_names=operand_vars,
            operand_codes=operand_codes,
        )

    def visitOr(self, ctx: LispParser.OrContext) -> ExpressionVisitResult:
        lisp_or = "or"
        c_name = self.__symbols.find_api_symbol(lisp_or)
        assert c_name is not None, f'Symbol "{lisp_or}" is not found'

        with self.__evaluable_ctx:
            operand_vars, operand_codes = self.__visit_operands(ctx.test())

        return self.__visit_function(
            function_name=c_name,
            operand_names=operand_vars,
            operand_codes=operand_codes,
        )

    def visitProcedureCall(
        self, ctx: LispParser.ProcedureCallContext
    ) -> ExpressionVisitResult:
        # TODO: add support of calling lambdas
        # TODO: если if, то получения значения должно быть evaluable (и не должно проверяться на этапе компиляции)

        operator_var, operator_code = self.visit(ctx.operator())
        operand_vars, operand_codes = self.__visit_operands(ctx.operand())

        expr_code = self.__code_creator.lambda_call()
        expr_var = self.__variable_manager.create_object_name()
        expr_code.update_data(var=expr_var, lambda_var=operator_var, args=operand_vars)

        wrapped_expr_code = wrap_codes(expr_code, [operator_code] + operand_codes)

        return expr_var, wrapped_expr_code

    def visitProcedure(self, ctx: LispParser.ProcedureContext) -> ExpressionVisitResult:
        env = self.__environment_ctx.env

        env_var = "env"  # TODO: прибито (из шаблона)

        formals = ctx.formals()
        body = ctx.procedureBody()

        function_code = self.__code_creator.lambda_definition()

        with self.__lambda_ctx, self.__environment_ctx:
            self.__environment_ctx.init(name=env_var, code=env.code)

            formals_text_before, formals_text_after = self.visitFormals(formals)
            body_var, body_code_text = self.visit(body)

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
            ret_var=body_var,
            body=body,
        )

        function_code.make_final()
        self.__declaration_ctx.add_declaration(function_code)

        lambda_var = self.__variable_manager.create_object_name()
        lambda_creation_code = self.__code_creator.make_lambda()
        lambda_creation_code.update_data(
            var=lambda_var, func=function_name, env=env.name
        )

        return lambda_var, lambda_creation_code

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

            param_var = self.__variable_manager.create_object_name()
            current_arg_getting_code = self.__code_creator.get_function_argument()
            current_arg_getting_code.update_data(index=i, var=param_var)

            current_arg_getting_code.make_final_final()
            codes.append(current_arg_getting_code)
            self.__lambda_ctx.add_param(param_name=param_lisp_name, param_var=param_var)

        return join_codes(codes), ""

    def visitListFormals(self, ctx: LispParser.ListFormalsContext) -> tuple[str, str]:
        # TODO: прибито
        count = "count"
        args = "args"

        param_lisp_name = ctx.variable().getText()
        if self.__symbols.has_api_symbol(param_lisp_name):
            raise ParamNameConflictException(param_lisp_name, ctx)

        arg_var = self.__variable_manager.create_object_name()
        arg_getting_code = self.__code_creator.make_list()
        arg_getting_code.update_data(var=arg_var, count=count, elements=args)

        arg_getting_code.make_final_final()

        secondary = arg_getting_code.render_secondary() + "\n"
        arg_getting_code.clear_secondary()

        self.__lambda_ctx.add_param(param_name=param_lisp_name, param_var=arg_var)

        return arg_getting_code.render(), secondary

    def visitVariadicFormals(
        self, ctx: LispParser.VariadicFormalsContext
    ) -> tuple[str, str]:
        # TODO: прибито
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

            current_arg_var = self.__variable_manager.create_object_name()
            current_arg_getting_code = self.__code_creator.get_function_argument()
            current_arg_getting_code.update_data(index=i, var=current_arg_var)

            current_arg_getting_code.make_final_final()
            codes_to_join.append(current_arg_getting_code)
            self.__lambda_ctx.add_param(
                param_name=param_lisp_name, param_var=current_arg_var
            )

        # Variadic
        variadic_lisp_name = variadic_variable.getText()
        if variadic_lisp_name in lisp_names:
            raise DuplicatedParamException(variadic_lisp_name, ctx)
        if self.__symbols.has_api_symbol(variadic_lisp_name):
            raise ParamNameConflictException(variadic_lisp_name, ctx)

        variadic_arg_var = self.__variable_manager.create_object_name()
        variadic_arg_getting_code = self.__code_creator.make_list()
        variadic_arg_getting_code.update_data(
            var=variadic_arg_var,
            count=f"{count}-{len(fixed_variables)}",
            elements=f"{args}+{len(fixed_variables)}",
        )
        variadic_arg_getting_code.make_final_final()

        self.__lambda_ctx.add_param(
            param_name=variadic_lisp_name, param_var=variadic_arg_var
        )

        secondary = variadic_arg_getting_code.render_secondary() + "\n"
        variadic_arg_getting_code.clear_secondary()
        codes_to_join.append(variadic_arg_getting_code)

        return join_codes(codes_to_join), secondary

    def visitBoolConstant(
        self, ctx: LispParser.BoolConstantContext
    ) -> ExpressionVisitResult:
        lisp_true = "#t"

        code = self.__code_creator.make_boolean()
        value = 1 if ctx.getText() == lisp_true else 0

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
        expr_var = self.__variable_manager.create_object_name()
        code.update_data(var=expr_var, value=value)

        return expr_var, code

    def __visit_function(
        self, function_name: str, operand_names: list[str], operand_codes: list[Code]
    ) -> ExpressionVisitResult:
        if self.__evaluable_ctx.should_make_evaluable:
            expr_code = self.__code_creator.make_evaluable()
        else:
            expr_code = self.__code_creator.procedure_call()

        expr_var = self.__variable_manager.create_object_name()
        expr_code.update_data(func=function_name, args=operand_names, var=expr_var)
        wrapped_expr_code = wrap_codes(expr_code, operand_codes)

        return expr_var, wrapped_expr_code

    def __visit_operands(self, operands) -> tuple[list[str], list[Code]]:
        operand_vars = []
        operand_codes = []

        for op in operands:
            op_var, op_template = self.visit(op)
            operand_vars.append(op_var)
            operand_codes.append(op_template)

        return operand_vars, operand_codes
