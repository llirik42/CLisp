from typing import Union

from src.LispParser import LispParser
from src.LispVisitor import LispVisitor
from src.rendering import (
    CodeCreator,
    wrap_codes,
    join_codes,
    transfer_secondary,
)
from src.rendering.codes import MakePrimitiveCode, Code
from src.symbols import Symbols
from .ast_context import ASTContext, visit
from .declarations_context import DeclarationsContext
from .environment_context import EnvironmentContext
from .exceptions import (
    UnexpectedIdentifierException,
    FunctionRedefineException,
    DuplicatedBindingException,
    DuplicatedParamException,
    ParamNameConflictException,
)
from .let_type_context import LetTypeContext, LetType
from .variable_manager import VariableManager

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

ast_context = ASTContext()


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

    @visit(ast_context)
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

    @visit(ast_context)
    def visitProcedure(self, ctx: LispParser.ProcedureContext) -> ExpressionVisitResult:
        env_var = self.__symbols.find_internal("lambda_env")
        env = self.__environment_ctx.env

        with self.__environment_ctx:
            self.__environment_ctx.init(name=env_var, code=env.code)
            formals_text = self.visit(ctx.procedureFormals())

            return self.__visit_lambda(
                formals_text=formals_text, body=ctx.procedureBody()
            )

    @visit(ast_context)
    def visitDelay(self, ctx: LispParser.DelayContext) -> ExpressionVisitResult:
        env_var = self.__symbols.find_internal("evaluable_env")
        env = self.__environment_ctx.env

        with self.__environment_ctx:
            self.__environment_ctx.init(name=env_var, code=env.code)

            return self.__visit_evaluable(ctx.expression())

    @visit(ast_context)
    def visitForce(self, ctx:LispParser.ForceContext) -> ExpressionVisitResult:
        expr_var, expr_code = self.visit(ctx.expression())

        force_var = self.__variable_manager.create_object_name()
        force_code = self.__code_creator.evaluation()
        force_code.update_data(var=force_var, evaluable_var=expr_var)

        return force_var, wrap_codes(force_code, expr_code)

    @visit(ast_context)
    def visitProcedureFixedFormals(
        self, ctx: LispParser.ProcedureFixedFormalsContext
    ) -> str:
        formals = [f.getText() for f in ctx.variable()]

        return self.__visit_formals(formals=formals, has_variadic_formal=False)

    @visit(ast_context)
    def visitProcedureVariadicFormal(
        self, ctx: LispParser.ProcedureVariadicFormalContext
    ) -> str:
        formal = ctx.variable().getText()

        return self.__visit_formals(formals=[formal], has_variadic_formal=True)

    @visit(ast_context)
    def visitProcedureMixedFormals(
        self, ctx: LispParser.ProcedureMixedFormalsContext
    ) -> str:
        formals = [f.getText() for f in ctx.variable()]

        return self.__visit_formals(formals=formals, has_variadic_formal=True)

    @visit(ast_context)
    def visitProcedureBody(
        self, ctx: LispParser.ProcedureBodyContext
    ) -> BodyVisitResult:
        definitions_codes = [self.visit(d)[1] for d in ctx.definition()]

        last_expr_var, expr_codes = self.__visit_lambda_expressions(ctx.expression())

        return (
            last_expr_var,
            join_codes(definitions_codes + expr_codes),
        )

    @visit(ast_context)
    def visitLet(self, ctx: LispParser.LetContext) -> ExpressionVisitResult:
        return self.__visit_let(let_type=LetType.LET)

    @visit(ast_context)
    def visitLetAsterisk(
        self, ctx: LispParser.LetAsteriskContext
    ) -> ExpressionVisitResult:
        return self.__visit_let(let_type=LetType.LET_ASTERISK)

    @visit(ast_context)
    def visitLetRec(self, ctx: LispParser.LetRecContext) -> ExpressionVisitResult:
        return self.__visit_let(let_type=LetType.LET_REC)

    @visit(ast_context)
    def visitBindingList(
        self, ctx: LispParser.BindingListContext
    ) -> list[BindingVisitResult]:
        variables_names = [b.variable().getText() for b in ctx.binding()]
        self.__check_binding_list(variables_names)

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

    @visit(ast_context)
    def visitBinding(self, ctx: LispParser.BindingContext) -> tuple[Code, str]:
        env = self.__environment_ctx.env
        variable_name = ctx.variable().getText()
        expression = ctx.expression()
        expr_var, expr_code = self.visit(expression)
        binding_code = self.__code_creator.set_variable_value()
        binding_code.update_data(
            env=env.name,
            name=variable_name,
            value=expr_var,
        )

        return wrap_codes(binding_code, expr_code), variable_name

    @visit(ast_context)
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

    @visit(ast_context)
    def visitProcedureDefinition(
        self, ctx: LispParser.ProcedureDefinitionContext
    ) -> ExpressionVisitResult:
        env_var = self.__symbols.find_internal("lambda_env")
        env = self.__environment_ctx.env

        variable_name = ctx.variable().getText()

        self.__check_variable_definition(variable_name)
        env.add(variable_name)

        with self.__environment_ctx:
            self.__environment_ctx.init(name=env_var, code=env.code)
            formals_text = self.visit(ctx.procedureDefinitionFormals())
            procedure_var, procedure_code = self.__visit_lambda(
                formals_text=formals_text, body=ctx.procedureBody()
            )

        return self.__visit_variable_definition(
            variable_name=variable_name,
            expr_var=procedure_var,
            expr_code=procedure_code,
        )

    @visit(ast_context)
    def visitProcedureDefinitionFixedFormals(
        self, ctx: LispParser.ProcedureDefinitionFixedFormalsContext
    ) -> str:
        formals = [f.getText() for f in ctx.variable()]

        return self.__visit_formals(formals=formals, has_variadic_formal=False)

    @visit(ast_context)
    def visitProcedureDefinitionVariadicFormal(
        self, ctx: LispParser.ProcedureDefinitionVariadicFormalContext
    ) -> str:
        formal = ctx.variable().getText()

        return self.__visit_formals(formals=[formal], has_variadic_formal=True)

    @visit(ast_context)
    def visitProcedureDefinitionMixedFormals(
        self, ctx: LispParser.ProcedureDefinitionMixedFormalsContext
    ) -> str:
        formals = [f.getText() for f in ctx.variable()]

        return self.__visit_formals(formals=formals, has_variadic_formal=True)

    @visit(ast_context)
    def visitVariableDefinition(
        self, ctx: LispParser.VariableDefinitionContext
    ) -> ExpressionVisitResult:
        variable_name = ctx.variable().getText()

        self.__check_variable_definition(variable_name=variable_name)
        self.__environment_ctx.env.add(variable_name)

        expression = ctx.expression()
        expr_var, expr_code = self.visit(expression)

        return self.__visit_variable_definition(
            variable_name=variable_name, expr_var=expr_var, expr_code=expr_code
        )

    @visit(ast_context)
    def visitAssignment(
        self, ctx: LispParser.AssignmentContext
    ) -> ExpressionVisitResult:
        expression = ctx.expression()
        variable_name = ctx.variable().getText()
        env = self.__environment_ctx.env

        if not env.has_variable_recursively(variable_name):
            raise UnexpectedIdentifierException(variable_name, ctx)

        expr_var, expr_code = self.visit(expression)

        assignment_var = self.__variable_manager.create_object_name()
        assignment_code = self.__code_creator.update_variable_value()
        assignment_code.update_data(
            var=assignment_var,
            env=env.name,
            name=variable_name,
            value=expr_var,
        )

        return assignment_var, wrap_codes(assignment_code, expr_code)

    @visit(ast_context)
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

    @visit(ast_context)
    def visitAnd(self, ctx: LispParser.AndContext) -> ExpressionVisitResult:
        return self.__visit_and(ctx.test())

    @visit(ast_context)
    def visitOr(self, ctx: LispParser.OrContext) -> ExpressionVisitResult:
        return self.__visit_or(ctx.test())

    @visit(ast_context)
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

    @visit(ast_context)
    def visitVariable(self, ctx: LispParser.VariableContext) -> ExpressionVisitResult:
        env = self.__environment_ctx.env
        variable_name = ctx.getText()

        if not env.has_variable_recursively(variable_name):
            raise UnexpectedIdentifierException(variable_name, ctx)

        expr_var = self.__variable_manager.create_object_name()
        expr_code = self.__code_creator.get_variable_value()
        expr_code.update_data(var=expr_var, env=env.name, name=variable_name)

        return expr_var, expr_code

    @visit(ast_context)
    def visitBoolConstant(
        self, ctx: LispParser.BoolConstantContext
    ) -> ExpressionVisitResult:
        lisp_true = "#t"
        return self.__visit_boolean(ctx.getText() == lisp_true)

    @visit(ast_context)
    def visitCharacterConstant(
        self, ctx: LispParser.CharacterConstantContext
    ) -> ExpressionVisitResult:
        value = f"{ctx.getText()[2:]}"

        if value == "'":
            value = "\\'"  # Escape single quote

        code = self.__code_creator.make_character()

        return self.__visit_constant(code=code, value=f"'{value}'")

    @visit(ast_context)
    def visitStringConstant(
        self, ctx: LispParser.StringConstantContext
    ) -> ExpressionVisitResult:
        code = self.__code_creator.make_string()

        return self.__visit_constant(code=code, value=ctx.getText())

    @visit(ast_context)
    def visitIntegerConstant(
        self, ctx: LispParser.IntegerConstantContext
    ) -> ExpressionVisitResult:
        code = self.__code_creator.make_int()

        return self.__visit_constant(code=code, value=int(ctx.getText()))

    @visit(ast_context)
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
            self.__environment_ctx.init(code=main_code, name=global_env_var)
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

        consequent_increase_ref_count_code = self.__code_creator.increase_ref_count()
        consequent_increase_ref_count_code.update_data(var=consequent_var)

        alternate_increase_ref_count_code = self.__code_creator.increase_ref_count()
        alternate_increase_ref_count_code.update_data(var=alternate_var)

        consequent_code = wrap_codes(
            consequent_increase_ref_count_code, consequent_code
        )
        alternate_code = wrap_codes(alternate_increase_ref_count_code, alternate_code)

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

        consequent_var, consequent_code = (op1_var, self.__code_creator.empty())

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
        formals_text: str,
        body: LispParser.ProcedureBodyContext,
    ) -> DeclaredFunctionName:
        function_code = self.__code_creator.lambda_definition()
        body_var, body_code_text = self.visit(body)
        function_name = self.__variable_manager.create_lambda_function_name()

        body = formals_text + "\n" if formals_text else ""
        body += body_code_text

        function_code.update_data(
            func=function_name,
            ret_var=body_var,
            body=body,
        )
        function_code.transfer_newline()

        self.__declaration_ctx.add_declaration(function_code)

        return function_name

    def __add_evaluable_declaration(
        self, expression: LispParser.ExpressionContext
    ) -> DeclaredFunctionName:
        function_code = self.__code_creator.evaluable_definition()
        expr_var, expr_code = self.visit(expression)
        expr_code.transfer_newline()

        function_name = self.__variable_manager.create_evaluable_function_name()

        result_increase_ref_count = self.__code_creator.increase_ref_count()
        result_increase_ref_count.update_data(var=expr_var)

        body = wrap_codes(result_increase_ref_count, expr_code).render()

        function_code.update_data(
            func=function_name,
            ret_var=expr_var,
            body=body,
        )

        self.__declaration_ctx.add_declaration(function_code)

        return function_name

    def __visit_formals(self, formals: list[str], has_variadic_formal: bool) -> str:
        self.__check_formals(formals)

        if has_variadic_formal:
            fixed_formals = formals[:-1]
            variadic_formal = formals[-1]
            variadic_formal_code = self.__visit_variadic_formal(
                formal=variadic_formal,
                start_index=len(fixed_formals),
            )
        else:
            fixed_formals = formals
            variadic_formal_code = self.__code_creator.empty()

        fixed_formals_codes = self.__visit_scalar_formals(fixed_formals)

        return join_codes(fixed_formals_codes + [variadic_formal_code])

    def __visit_scalar_formals(self, formals: list[str]) -> list[Code]:
        args_name = self.__symbols.find_internal("lambda_args")

        env = self.__environment_ctx.env
        codes = []

        for i, param_name in enumerate(formals):
            current_arg_code = self.__code_creator.set_variable_value()
            current_arg_code.update_data(
                env=env.name, name=param_name, value=f"{args_name}[{i}]"
            )
            env.add(param_name)

            current_arg_code.remove_newlines()
            codes.append(current_arg_code)

        return codes

    def __visit_variadic_formal(
        self,
        formal: str,
        start_index: int,
    ) -> VariadicFormalVisitResult:
        count_name = self.__symbols.find_internal("lambda_count")
        args_name = self.__symbols.find_internal("lambda_args")

        env = self.__environment_ctx.env
        variadic_formal_list_var = self.__variable_manager.create_object_name()

        if start_index == 0:
            count = count_name
            args = args_name
        else:
            count = f"{count_name}-{start_index}"
            args = f"{args_name}+{start_index}"

        variadic_formal_list_code = self.__code_creator.make_list_from_array()
        variadic_formal_list_code.update_data(
            var=variadic_formal_list_var, count=count, elements=args
        )

        code = self.__code_creator.set_variable_value()
        code.update_data(env=env.name, name=formal, value=variadic_formal_list_var)
        env.add(formal)

        return wrap_codes(code, variadic_formal_list_code)

    def __visit_lambda_expressions(
        self, expressions: list[LispParser.ExpressionContext]
    ) -> LambdaExpressionsVisitResult:
        last_expr_var = ""
        expr_codes = []

        for i, e in enumerate(expressions):
            e_var, e_code = self.visit(e)

            is_expression_last = i == len(expressions) - 1
            if is_expression_last:
                increase_ref_count_count_code = self.__code_creator.increase_ref_count()
                increase_ref_count_count_code.update_data(var=e_var)
                increase_ref_count_count_code.remove_newlines()
                e_code.add_secondary_prolog(
                    "\n" + increase_ref_count_count_code.render()
                )

            e_code.transfer_newline()
            last_expr_var = e_var
            expr_codes.append(e_code)

        return last_expr_var, expr_codes

    def __visit_let(
        self,
        let_type: LetType,
    ) -> ExpressionVisitResult:
        env = self.__environment_ctx.env
        ctx = ast_context.ctx  # LetContext/LetAsteriskContext/LetRecContext

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

    def __visit_lambda(
        self, formals_text: str, body: LispParser.ProcedureBodyContext
    ) -> ExpressionVisitResult:
        parent_env = self.__environment_ctx.env.parent

        function_name = self.__add_lambda_declaration(
            formals_text=formals_text,
            body=body,
        )

        lambda_var = self.__variable_manager.create_object_name()
        lambda_creation_code = self.__code_creator.make_lambda()
        lambda_creation_code.update_data(
            var=lambda_var, func=function_name, env=parent_env.name
        )

        return lambda_var, lambda_creation_code

    def __visit_evaluable(
        self, expression: LispParser.ExpressionContext
    ) -> ExpressionVisitResult:
        parent_env = self.__environment_ctx.env.parent

        function_name = self.__add_evaluable_declaration(expression)

        evaluable_var = self.__variable_manager.create_object_name()
        evaluable_creation_code = self.__code_creator.make_evaluable()
        evaluable_creation_code.update_data(
            var=evaluable_var, func=function_name, env=parent_env.name
        )

        return evaluable_var, evaluable_creation_code

    def __visit_variable_definition(
        self, variable_name: str, expr_var: str, expr_code: Code
    ) -> ExpressionVisitResult:
        env = self.__environment_ctx.env

        definition_code = self.__code_creator.set_variable_value()
        definition_code.update_data(
            env=env.name,
            name=variable_name,
            value=expr_var,
        )

        # First element is ignored and needed to unify the processing of expressions and definitions
        return "", wrap_codes(definition_code, expr_code)

    def __check_binding_list(self, variables_names: list[str]) -> None:
        ctx = ast_context.ctx
        visited_variables = set()

        for v in variables_names:
            if self.__symbols.has_api_symbol(v):
                raise FunctionRedefineException(v, ctx)

            if v in visited_variables:
                raise DuplicatedBindingException(v, ctx)

            visited_variables.add(v)

    def __check_formals(self, formals: list[str]) -> None:
        ctx = ast_context.ctx
        visited_formals = set()

        for f in formals:
            if self.__symbols.has_api_symbol(f):
                raise ParamNameConflictException(f, ctx)

            if f in visited_formals:
                raise DuplicatedParamException(f, ctx)

            visited_formals.add(f)

    def __check_variable_definition(self, variable_name: str) -> None:
        if self.__symbols.has_api_symbol(variable_name):
            raise FunctionRedefineException(variable_name, ast_context.ctx)
