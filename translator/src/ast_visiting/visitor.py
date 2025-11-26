from typing import Union

from antlr4 import ParserRuleContext

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
from .let_type_context import LetTypeContext, LetType
from .variable_manager import VariableManager
from .exceptions import (
    UnexpectedIdentifierException,
    FunctionRedefineException,
    DuplicatedBindingException,
    DuplicatedParamException,
    ParamNameConflictException,
)
from src.rendering.codes import MakePrimitiveCode, Code
from ..environment import Environment

# (variable, code)
ExpressionVisitResult = tuple[str, Code]

# ([var1, var2, ..., varn], (code1, code2, ..., coden) - same as in the ExpressionVisitResult
OperandsVisitResult = tuple[list[str], list[Code]]

# (variable that matches the last expression, code)
BodyVisitResult = tuple[str, str]

# Code of creating value of the variable and binding it
BindingVisitResult = Code

# Text of the output C-program
ProgramVisitResult = str

# Name of the function that was declared
DeclaredFunctionName = str

# List of the codes for each visited program element
ProgramElementsVisitResult = list[Code]

# For each visited definition there is a secondary part of its code (in first tuple element) and its code without secondary part (in second tuple element)
LambdaDefinitionsVisitResult = tuple[list[str], list[Code]]

# (variable of the last expression, list of the codes for each expression)
LambdaExpressionsVisitResult = tuple[str, list[Code]]

# (Codes for every fixed formal, names of the parameters)
FixedFormalsVisitResult = tuple[list[Code], list[str]]

# (code of the formal without secondary, secondary part of the code)
VariadicFormalVisitResult = tuple[Code, str]


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
        self.__let_type_ctx = LetTypeContext()

    def visitProgram(self, ctx: LispParser.ProgramContext) -> ProgramVisitResult:
        global_env_var = self.__variable_manager.create_environment_name()
        main_code = self.__code_creator.get_global_environment()
        main_code.update_data(var=global_env_var)

        program_element_codes = self.__visit_program_elements(
            main_code=main_code,
            global_env_var=global_env_var,
            elements=ctx.programElement(),
        )

        for c in program_element_codes:
            c.transfer_newline()
        if len(program_element_codes) != 0:
            main_code.add_main_epilog(f"\n{join_codes(program_element_codes)}")

        program_code = self.__code_creator.program()
        program_code.update_data(
            declarations=[
                c.render() for c in self.__declaration_ctx.iter_declarations()
            ],
            main_body=main_code.render(),
        )

        return program_code.render()

    def visitProcedure(self, ctx: LispParser.ProcedureContext) -> ExpressionVisitResult:
        env = self.__environment_ctx.env

        function_name = self.__add_lambda_declaration(
            formals=ctx.formals(), body=ctx.procedureBody()
        )

        lambda_var = self.__variable_manager.create_object_name()
        lambda_creation_code = self.__code_creator.make_lambda()
        lambda_creation_code.update_data(
            var=lambda_var, func=function_name, env=env.name
        )

        return lambda_var, lambda_creation_code

    def visitFixedFormals(self, ctx: LispParser.FixedFormalsContext) -> tuple[str, str]:
        codes, _ = self.__visit_scalar_formals(ctx.variable(), ctx)

        return join_codes(codes), ""

    def visitListFormals(self, ctx: LispParser.ListFormalsContext) -> tuple[str, str]:
        code, secondary = self.__visit_variadic_formal(
            ctx.variable(), ctx, start_index=0, already_visited_params=[]
        )

        return code.render(), secondary

    def visitVariadicFormals(
        self, ctx: LispParser.VariadicFormalsContext
    ) -> tuple[str, str]:
        fixed_variables = ctx.variable()[:-1]
        variadic_variable = ctx.variable()[-1]

        fixed_formals_codes, visited_fixed_params = self.__visit_scalar_formals(
            variables=fixed_variables, ctx=ctx
        )
        variadic_formal_code, list_formal_secondary = self.__visit_variadic_formal(
            variable=variadic_variable,
            ctx=ctx,
            start_index=len(fixed_variables),
            already_visited_params=visited_fixed_params,
        )

        return (
            join_codes(fixed_formals_codes + [variadic_formal_code]),
            list_formal_secondary,
        )

    def visitProcedureBody(
        self, ctx: LispParser.ProcedureBodyContext
    ) -> BodyVisitResult:
        definitions_secondary, definitions_codes = self.__visit_lambda_definitions(
            ctx.procedureBodyDefinition()
        )

        last_expr_var, expr_codes = self.__visit_lambda_expressions(ctx.expression())

        if definitions_secondary:
            definitions_secondary_text = "\n".join(definitions_secondary) + "\n"
        else:
            definitions_secondary_text = ""

        return (
            last_expr_var,
            join_codes(definitions_codes + expr_codes) + definitions_secondary_text,
        )

    def visitProcedureBodyDefinition(
        self, ctx: LispParser.ProcedureBodyDefinitionContext
    ) -> Code:
        expression = ctx.definition().expression()
        variable = ctx.definition().variable()

        expr_var, expr_code = self.visit(expression)
        expr_code.remove_newlines()
        self.__lambda_ctx.set_param_var(variable.getText(), expr_var)

        return expr_code

    def visitLet(self, ctx: LispParser.LetContext) -> ExpressionVisitResult:
        return self.__visit_let(let_type=LetType.LET, ctx=ctx)

    def visitLetAsterisk(
        self, ctx: LispParser.LetAsteriskContext
    ) -> ExpressionVisitResult:
        return self.__visit_let(let_type=LetType.LET_ASTERISK, ctx=ctx)

    def visitLetRec(self, ctx: LispParser.LetRecContext) -> ExpressionVisitResult:
        return self.__visit_let(let_type=LetType.LET_REC, ctx=ctx)

    def visitBindingList(
        self, ctx: LispParser.BindingListContext
    ) -> list[BindingVisitResult]:
        result = [self.visit(b) for b in ctx.binding()]
        if self.__let_type_ctx.type_ != LetType.LET:
            # All variables have already been added to the environment (let*, letrec)
            return result

        # No variables were added (let)
        env = self.__environment_ctx.env
        for b in ctx.binding():
            variable_name = b.variable().getText()

            if env.has_variable(variable_name):
                raise DuplicatedBindingException(variable_name, ctx)

            env.add_variable(variable_name)

        return result

    def visitBinding(self, ctx: LispParser.BindingContext) -> BindingVisitResult:
        env = self.__environment_ctx.env

        variable_name = ctx.variable().getText()

        if self.__symbols.has_api_symbol(variable_name):
            raise FunctionRedefineException(variable_name, ctx)

        if env.has_variable(variable_name):
            raise DuplicatedBindingException(variable_name, ctx)

        expression = ctx.expression()

        expr_code = expr_var = None
        match self.__let_type_ctx.type_:
            case LetType.LET:
                expr_var, expr_code = self.visit(expression)
            case LetType.LET_ASTERISK:
                expr_var, expr_code = self.visit(expression)
                env.add_variable(variable_name)
            case LetType.LET_REC:
                env.add_variable(variable_name)
                expr_var, expr_code = self.visit(expression)
            case _:
                raise RuntimeError("Unknown type of let")

        expr_code.remove_first_secondary_line()

        binding_code = self.__code_creator.set_variable_value()
        binding_code.update_data(
            env=env.name,
            name=f'"{variable_name}"',
            value=expr_var,
        )

        return wrap_codes(binding_code, expr_code)

    def visitEnvironmentBody(
        self, ctx: LispParser.EnvironmentBodyContext
    ) -> BodyVisitResult:
        body_codes = []

        for d in ctx.environmentBodyDefinition():
            _, d_code = self.visit(d)
            body_codes.append(d_code)

        env = self.__environment_ctx.env
        expressions = ctx.expression()
        expr_vars = []

        for e in expressions:
            e_var, e_code = self.visit(e)
            transfer_secondary(e_code, env.code)

            expr_vars.append(e_var)
            body_codes.append(e_code)

        return expr_vars[-1], join_codes(body_codes)

    def visitEnvironmentBodyDefinition(
        self, ctx: LispParser.EnvironmentBodyDefinitionContext
    ) -> ExpressionVisitResult:
        env = self.__environment_ctx.env

        variable_name = ctx.definition().variable().getText()
        if self.__symbols.has_api_symbol(variable_name):
            raise FunctionRedefineException(variable_name, ctx)

        expression = ctx.definition().expression()
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
        expression = ctx.expression()
        variable_name = ctx.variable().getText()
        env = self.__environment_ctx.env
        is_env_top_level_lambda = (
            env.parent and env.parent.is_global and self.__lambda_ctx.inside_lambda
        )

        # Attempt of changing lambda param
        if is_env_top_level_lambda and self.__lambda_ctx.has_param(variable_name):
            return self.__visit_lambda_param_assignment(
                param_name=variable_name, expression=expression
            )

        # Attempt of changing environment variable
        if env.has_variable_recursively(variable_name):
            return self.__visit_environment_variable_assignment(
                env=env, variable_name=variable_name, expression=expression
            )

        # Attempt of changing lambda param from environment created in lambda
        if self.__lambda_ctx.inside_lambda and self.__lambda_ctx.has_param(
            variable_name
        ):
            return self.__visit_lambda_param_assignment(
                param_name=variable_name, expression=expression
            )

        raise UnexpectedIdentifierException(variable_name, ctx)

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
        # TODO: wrap lambda call into evaluable in if, and, or.

        operator_var, operator_code = self.visit(ctx.operator())
        operand_vars, operand_codes = self.__visit_operands(ctx.operand())

        expr_code = self.__code_creator.lambda_call()
        expr_var = self.__variable_manager.create_object_name()
        expr_code.update_data(var=expr_var, lambda_var=operator_var, args=operand_vars)

        wrapped_expr_code = wrap_codes(expr_code, [operator_code] + operand_codes)

        return expr_var, wrapped_expr_code

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

    def __visit_program_elements(
        self,
        main_code: Code,
        global_env_var: str,
        elements: list[LispParser.ProgramElementContext],
    ) -> ProgramElementsVisitResult:
        with self.__environment_ctx:
            self.__environment_ctx.init(
                code=main_code, name=global_env_var, is_global=True
            )
            env = self.__environment_ctx.env

            for lisp_name, _ in self.__symbols.find_api_function_items():
                env.add_variable(lisp_name)

            return [self.visit(e)[1] for e in elements]

    def __add_lambda_declaration(
        self,
        formals: LispParser.FormalsContext,
        body: LispParser.ProcedureBodyContext,
    ) -> DeclaredFunctionName:
        env_var = "env"  # variable that stores environment in the lambda function (from the template)
        env = self.__environment_ctx.env

        function_code = self.__code_creator.lambda_definition()

        # Visiting formals of the procedure
        with self.__lambda_ctx, self.__environment_ctx:
            self.__environment_ctx.init(name=env_var, code=env.code)
            formals_text_before, formals_text_after = self.visitFormals(formals)
            body_var, body_code_text = self.visit(body)

        function_name = self.__variable_manager.create_function_name()

        body = formals_text_before + "\n" if formals_text_before else ""
        body += body_code_text
        body += formals_text_after

        function_code.update_data(
            func=function_name,
            ret_var=body_var,
            body=body,
        )
        function_code.transfer_newline()

        self.__declaration_ctx.add_declaration(function_code)

        return function_name

    def __visit_scalar_formals(
        self, variables: list[LispParser.VariableContext], ctx: ParserRuleContext
    ) -> FixedFormalsVisitResult:
        codes = []
        visited_params = []

        for i, v in enumerate(variables):
            param_lisp_name = v.getText()

            if param_lisp_name in visited_params:
                raise DuplicatedParamException(param_lisp_name, ctx)
            if self.__symbols.has_api_symbol(param_lisp_name):
                raise ParamNameConflictException(param_lisp_name, ctx)

            visited_params.append(param_lisp_name)

            param_var = self.__variable_manager.create_object_name()
            current_arg_getting_code = self.__code_creator.get_function_argument()
            current_arg_getting_code.update_data(index=i, var=param_var)

            current_arg_getting_code.remove_newlines()
            codes.append(current_arg_getting_code)
            self.__lambda_ctx.set_param_var(
                param_name=param_lisp_name, param_var=param_var
            )

        return codes, visited_params

    def __visit_variadic_formal(
        self,
        variable: LispParser.VariableContext,
        ctx: ParserRuleContext,
        start_index: int,
        already_visited_params: list[str],
    ) -> VariadicFormalVisitResult:
        # variables that store number of args and the args in the lambda function (from the template)
        count_name = "count"
        args_name = "args"

        param_lisp_name = variable.getText()
        if param_lisp_name in already_visited_params:
            raise DuplicatedParamException(param_lisp_name, ctx)
        if self.__symbols.has_api_symbol(param_lisp_name):
            raise ParamNameConflictException(param_lisp_name, ctx)

        arg_var = self.__variable_manager.create_object_name()
        code = self.__code_creator.make_list()

        if start_index:
            count = f"{count_name}-{start_index}"
            elements = f"{args_name}+{start_index}"
        else:
            count = count_name
            elements = args_name

        code.update_data(var=arg_var, count=count, elements=elements)

        code.remove_newlines()

        secondary = code.render_secondary() + "\n"
        code.clear_secondary()

        self.__lambda_ctx.set_param_var(param_name=param_lisp_name, param_var=arg_var)

        return code, secondary

    def __visit_lambda_definitions(
        self, definitions: list[LispParser.ProcedureBodyDefinitionContext]
    ) -> LambdaDefinitionsVisitResult:
        definitions_secondary = []
        definitions_codes = []

        for d in definitions:
            d_code: Code = self.visit(d)
            definitions_secondary.append(d_code.render_secondary())
            d_code.clear_secondary()
            definitions_codes.append(d_code)

        return definitions_secondary, definitions_codes

    def __visit_lambda_expressions(
        self, expressions: list[LispParser.ExpressionContext]
    ) -> LambdaExpressionsVisitResult:
        last_expr_var = ""
        expr_codes = []

        for i, e in enumerate(expressions):
            e_var, e_code = self.visit(e)

            is_expression_last = i == len(expressions) - 1
            if is_expression_last:
                e_code.remove_first_secondary_line()  # Remove destroying result of the procedure

            e_code.transfer_newline()
            last_expr_var = e_var
            expr_codes.append(e_code)

        return last_expr_var, expr_codes

    def __visit_lambda_param_assignment(
        self, param_name: str, expression: LispParser.ExpressionContext
    ) -> ExpressionVisitResult:
        expr_var, expr_code = self.visit(expression)
        expr_code.remove_first_secondary_line()
        self.__lambda_ctx.set_param_var(param_name=param_name, param_var=expr_var)
        return expr_var, wrap_codes(self.__code_creator.empty(), expr_code)

    def __visit_environment_variable_assignment(
        self,
        env: Environment,
        variable_name: str,
        expression: LispParser.ExpressionContext,
    ) -> ExpressionVisitResult:
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

    def __visit_let(
        self,
        let_type: LetType,
        ctx: Union[
            LispParser.LetContext,
            LispParser.LetAsteriskContext,
            LispParser.LetRecContext,
        ],
    ) -> ExpressionVisitResult:
        env = self.__environment_ctx.env

        new_env_var = self.__variable_manager.create_environment_name()
        new_env_code = self.__code_creator.make_environment()
        new_env_code.update_data(var=new_env_var, parent=env.name)

        binding_list = ctx.bindingList()

        with self.__environment_ctx:
            self.__environment_ctx.init(code=new_env_code, name=new_env_var)
            self.__let_type_ctx.visit(let_type)

            bindings_codes = [c for c in self.visit(binding_list)]
            body_var, body_code = self.visit(ctx.environmentBody())

            joined_bindings_codes = join_codes(bindings_codes).replace("\n\n", "\n")
            new_env_code.add_main_epilog(f"{joined_bindings_codes}\n{body_code}")

        return body_var, new_env_code

    def __visit_let_binding(self):
        pass

    def __visit_letrec_binding(self):
        pass

    def __visit_let_asterisk_binding(self):
        pass

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

    def __visit_operands(self, operands) -> OperandsVisitResult:
        operand_vars = []
        operand_codes = []

        for op in operands:
            op_var, op_template = self.visit(op)
            operand_vars.append(op_var)
            operand_codes.append(op_template)

        return operand_vars, operand_codes
