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
VariadicFormalVisitResult = Code


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
        self.__environment_ctx = EnvironmentContext()
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
            formals=ctx.procedureFormals(), body=ctx.procedureBody()
        )

        lambda_var = self.__variable_manager.create_object_name()
        lambda_creation_code = self.__code_creator.make_lambda()
        lambda_creation_code.update_data(
            var=lambda_var, func=function_name, env=env.name
        )

        return lambda_var, lambda_creation_code

    def visitProcedureFixedFormals(self, ctx: LispParser.ProcedureFixedFormalsContext) -> tuple[str, str]:
        codes, _ = self.__visit_scalar_formals(ctx.variable(), ctx)

        return join_codes(codes), ""

    def visitProcedureVariadicFormal(self, ctx: LispParser.ProcedureVariadicFormalContext) -> tuple[str, str]:
        code = self.__visit_variadic_formal(
            ctx.variable(), ctx, start_index=0, already_visited_params=[]
        )

        return code.render(), ""

    def visitProcedureMixedFormals(
        self, ctx: LispParser.ProcedureMixedFormalsContext
    ) -> tuple[str, str]:
        fixed_variables = ctx.variable()[:-1]
        variadic_variable = ctx.variable()[-1]

        fixed_formals_codes, visited_fixed_params = self.__visit_scalar_formals(
            variables=fixed_variables, ctx=ctx
        )
        variadic_formal_code = self.__visit_variadic_formal(
            variable=variadic_variable,
            ctx=ctx,
            start_index=len(fixed_variables),
            already_visited_params=visited_fixed_params,
        )

        return (
            join_codes(fixed_formals_codes + [variadic_formal_code]),
            "",
        )

    def visitProcedureBody(
        self, ctx: LispParser.ProcedureBodyContext
    ) -> BodyVisitResult:
        definitions_codes = [self.visit(d)[1] for d in ctx.definition()]

        last_expr_var, expr_codes = self.__visit_lambda_expressions(ctx.expression())

        return (
            last_expr_var,
            join_codes(definitions_codes + expr_codes),
        )

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
        variables_names = [b.variable().getText() for b in ctx.binding()]
        self.__check_binding_list_variables(variables_names, ctx)

        let_type = self.__let_type_ctx.type_
        env = self.__environment_ctx.env

        binding_list_codes = []

        if let_type is LetType.LET:
            for binding in ctx.binding():
                binding_code, _ = self.visit(binding)
                binding_list_codes.append(binding_code)
            env.extend(variables_names)

        if let_type is LetType.LET_ASTERISK:
            for binding in ctx.binding():
                binding_code, binding_variable_name = self.visit(binding)
                binding_list_codes.append(binding_code)
                env.add(binding_variable_name)

        if let_type is LetType.LET_REC:
            env.extend(variables_names)
            for binding in ctx.binding():
                binding_code, _ = self.visit(binding)
                binding_list_codes.append(binding_code)

        return binding_list_codes

    def visitBinding(self, ctx:LispParser.BindingContext) -> tuple[Code, str]:
        env = self.__environment_ctx.env
        variable_name = ctx.variable().getText()
        expression = ctx.expression()
        expr_var, expr_code = self.visit(expression)
        #expr_code.remove_first_secondary_line()
        binding_code = self.__code_creator.set_variable_value()
        binding_code.update_data(
            env=env.name,
            name=variable_name,
            value=expr_var,
        )

        return wrap_codes(binding_code, expr_code), variable_name

    def visitEnvironmentBody(
        self, ctx: LispParser.EnvironmentBodyContext
    ) -> BodyVisitResult:
        body_codes = []

        for d in ctx.definition():
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

    def visitDefinition(
        self, ctx: LispParser.DefinitionContext
    ) -> ExpressionVisitResult:
        env = self.__environment_ctx.env

        # TODO: handle procedureDefinition
        variable_definition = ctx.variableDefinition()

        variable_name = variable_definition.variable().getText()
        if self.__symbols.has_api_symbol(variable_name):
            raise FunctionRedefineException(variable_name, ctx)
        env.add(variable_name)

        expression = variable_definition.expression()
        expr_var, expr_code = self.visit(expression)
        #expr_code.remove_first_secondary_line()

        definition_code = self.__code_creator.set_variable_value()
        definition_code.update_data(
            env=env.name,
            name=variable_name,
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

        if not env.has_variable_recursively(variable_name):
            raise UnexpectedIdentifierException(variable_name, ctx)

        expr_var, expr_code = self.visit(expression)

        #expr_code.remove_first_secondary_line()

        assignment_var = self.__variable_manager.create_object_name()
        assignment_code = self.__code_creator.update_variable_value()
        assignment_code.update_data(
            var=assignment_var,
            env=env.name,
            name=variable_name,
            value=expr_var,
        )

        return assignment_var, wrap_codes(assignment_code, expr_code)

    def visitCondition(self, ctx: LispParser.ConditionContext) -> ExpressionVisitResult:
        test = ctx.test()
        consequent = ctx.consequent()
        alternate = ctx.alternate()

        test_var, test_code = self.visit(test)
        consequent_var, consequent_code = self.visit(consequent)

        if alternate:
            alternate_var, alternate_code = self.visit(alternate)
        else:
            alternate_var = self.__variable_manager.create_object_name()
            alternate_code = self.__code_creator.make_unspecified()
            alternate_code.update_data(var=alternate_var)

        return self.__visit_if(
            test_var=test_var,
            test_code=test_code,
            consequent_var=consequent_var,
            consequent_code=consequent_code,
            alternate_var=alternate_var,
            alternate_code=alternate_code,
        )

    def visitAnd(self, ctx: LispParser.AndContext) -> ExpressionVisitResult:
        return self.__visit_and(ctx.test())

    def visitOr(self, ctx: LispParser.OrContext) -> ExpressionVisitResult:
        return self.__visit_or(ctx.test())

    def visitProcedureCall(
        self, ctx: LispParser.ProcedureCallContext
    ) -> ExpressionVisitResult:
        operator_var, operator_code = self.visit(ctx.operator())
        operand_vars, operand_codes = self.__visit_operands(ctx.operand())

        expr_code = self.__code_creator.lambda_call()
        expr_var = self.__variable_manager.create_object_name()
        expr_code.update_data(var=expr_var, lambda_var=operator_var, args=operand_vars)

        wrapped_expr_code = wrap_codes(expr_code, [operator_code] + operand_codes)

        return expr_var, wrapped_expr_code

    def visitVariable(self, ctx: LispParser.VariableContext) -> ExpressionVisitResult:
        env = self.__environment_ctx.env
        variable_name = ctx.getText()

        if not env.has_variable_recursively(variable_name):
            raise UnexpectedIdentifierException(variable_name, ctx)

        expr_var = self.__variable_manager.create_object_name()
        expr_code = self.__code_creator.get_variable_value()
        expr_code.update_data(var=expr_var, env=env.name, name=variable_name)

        return expr_var, expr_code

    def visitBoolConstant(
        self, ctx: LispParser.BoolConstantContext
    ) -> ExpressionVisitResult:
        lisp_true = "#t"
        return self.__visit_boolean(ctx.getText() == lisp_true)

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
                code=main_code, name=global_env_var
            )
            env = self.__environment_ctx.env

            for lisp_name, _ in self.__symbols.find_api_function_items():
                env.add(lisp_name)

            return [self.visit(e)[1] for e in elements]

    def __visit_if(
        self,
        test_var: str,
        test_code: Code,
        consequent_var: str,
        consequent_code: Code,
        alternate_var: str,
        alternate_code: Code,
    ) -> ExpressionVisitResult:
        var = self.__variable_manager.create_object_name()
        code = self.__code_creator.if_()

        consequent_code.add_secondary_prolog(f"cl_increase_ref_count({consequent_var});")
        alternate_code.add_secondary_prolog(f"cl_increase_ref_count({alternate_var});")

        code.update_data(
            var=var,
            cond_var=test_var,
            then_var=consequent_var,
            else_var=alternate_var,
            then_body=consequent_code.render(),
            else_body=alternate_code.render(),
            pre_body=test_code.render_main(),
            post_body=test_code.render_secondary(),
        )

        return var, code

    def __visit_and(
        self, operands: list[LispParser.ExpressionContext]
    ) -> ExpressionVisitResult:
        if not operands:
            var = self.__variable_manager.create_object_name()
            code = self.__code_creator.make_true()
            code.update_data(var=var)
            return var, code

        if len(operands) == 1:
            return self.visit(operands[0])

        if len(operands) == 2:
            op1_var, op1_code = self.visit(operands[0])
            op2_var, op2_code = self.visit(operands[1])
            return self.__visit_and2(op1_var, op1_code, op2_var, op2_code)

        op1_var, op1_code = self.visit(operands[0])
        op2_var, op2_code = self.__visit_and(operands[1:])

        return self.__visit_and2(op1_var, op1_code, op2_var, op2_code)

    def __visit_and2(
        self, op1_var: str, op1_code: Code, op2_var: str, op2_code: Code
    ) -> ExpressionVisitResult:
        test_var, test_code = op1_var, op1_code
        consequent_var, consequent_code = op2_var, op2_code
        alternate_var, alternate_code = self.__visit_boolean(False)

        return self.__visit_if(
            test_var=test_var,
            test_code=test_code,
            consequent_var=consequent_var,
            consequent_code=consequent_code,
            alternate_var=alternate_var,
            alternate_code=alternate_code,
        )

    def __visit_or(
        self, operands: list[LispParser.ExpressionContext]
    ) -> ExpressionVisitResult:
        if not operands:
            var = self.__variable_manager.create_object_name()
            code = self.__code_creator.make_false()
            code.update_data(var=var)
            return var, code

        if len(operands) == 1:
            return self.visit(operands[0])

        if len(operands) == 2:
            op1_var, op1_code = self.visit(operands[0])
            op2_var, op2_code = self.visit(operands[1])
            return self.__visit_or2(op1_var, op1_code, op2_var, op2_code)

        op1_var, op1_code = self.visit(operands[0])
        op2_var, op2_code = self.__visit_or(operands[1:])

        return self.__visit_or2(op1_var, op1_code, op2_var, op2_code)

    def __visit_or2(
        self, op1_var: str, op1_code: Code, op2_var: str, op2_code: Code
    ) -> ExpressionVisitResult:
        test_var, test_code = op1_var, op1_code

        consequent_var, consequent_code = (
            op1_var,
            self.__code_creator.increase_ref_count(),
        )
        consequent_code.update_data(var=consequent_var)

        alternate_var, alternate_code = op2_var, op2_code

        return self.__visit_if(
            test_var=test_var,
            test_code=test_code,
            consequent_var=consequent_var,
            consequent_code=consequent_code,
            alternate_var=alternate_var,
            alternate_code=alternate_code,
        )

    def __add_lambda_declaration(
        self,
        formals: LispParser.ProcedureFormalsContext,
        body: LispParser.ProcedureBodyContext,
    ) -> DeclaredFunctionName:
        env_var = "env"  # variable that stores environment in the lambda function (from the template)
        env = self.__environment_ctx.env

        function_code = self.__code_creator.lambda_definition()

        # Visiting formals of the procedure
        with self.__environment_ctx:
            self.__environment_ctx.init(name=env_var, code=env.code)
            formals_text_before, formals_text_after = self.visit(formals)
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
        env = self.__environment_ctx.env

        codes = []
        visited_params = []

        for i, v in enumerate(variables):
            param_name = v.getText()

            if param_name in visited_params:
                raise DuplicatedParamException(param_name, ctx)
            if self.__symbols.has_api_symbol(param_name):
                raise ParamNameConflictException(param_name, ctx)

            visited_params.append(param_name)

            current_arg_code = self.__code_creator.set_variable_value()
            current_arg_code.update_data(env=env.name, name=param_name, value=f"args[{i}]")  # TODO: value прибито
            env.add(param_name)

            current_arg_code.remove_newlines()
            codes.append(current_arg_code)

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

        env = self.__environment_ctx.env

        param_name = variable.getText()
        if param_name in already_visited_params:
            raise DuplicatedParamException(param_name, ctx)
        if self.__symbols.has_api_symbol(param_name):
            raise ParamNameConflictException(param_name, ctx)

        value = f"cl_make_list_from_array({count_name}-{start_index}, {args_name}+{start_index})" # TODO: прибито

        code = self.__code_creator.set_variable_value()
        code.update_data(env=env.name, name=param_name, value=value)
        env.add(param_name)

        return code

    def __visit_lambda_expressions(
        self, expressions: list[LispParser.ExpressionContext]
    ) -> LambdaExpressionsVisitResult:
        last_expr_var = ""
        expr_codes = []

        for i, e in enumerate(expressions):
            e_var, e_code = self.visit(e)

            is_expression_last = i == len(expressions) - 1
            if is_expression_last:
                e_code.add_secondary_prolog(f"\ncl_increase_ref_count({e_var});") # TODO: прибито

            e_code.transfer_newline()
            last_expr_var = e_var
            expr_codes.append(e_code)

        return last_expr_var, expr_codes

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

    def __visit_constant(
        self, code: MakePrimitiveCode, value: Union[str, int, float]
    ) -> ExpressionVisitResult:
        expr_var = self.__variable_manager.create_object_name()
        code.update_data(var=expr_var, value=value)

        return expr_var, code

    def __visit_operands(self, operands) -> OperandsVisitResult:
        operand_vars = []
        operand_codes = []

        for op in operands:
            op_var, op_template = self.visit(op)
            operand_vars.append(op_var)
            operand_codes.append(op_template)

        return operand_vars, operand_codes

    def __visit_boolean(self, value: bool) -> ExpressionVisitResult:
        if value:
            code = self.__code_creator.make_true()
        else:
            code = self.__code_creator.make_false()

        var = self.__variable_manager.create_object_name()
        code.update_data(var=var)

        return var, code

    def __check_binding_list_variables(self, variables_names: list[str], ctx: ParserRuleContext) -> None:
        visited_variables = set()

        for v in variables_names:
            if self.__symbols.has_api_symbol(v):
                raise FunctionRedefineException(v, ctx)

            if v in visited_variables:
                raise DuplicatedBindingException(v, ctx)

            visited_variables.add(v)

