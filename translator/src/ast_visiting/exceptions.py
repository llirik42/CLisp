from antlr4 import ParserRuleContext


class VisitingException(Exception):
    def __init__(self, message: str, ctx: ParserRuleContext):
        """
        Class represents an exception that can be thrown during visiting of AST.

        :param message: message.
        :param ctx: context of the visiting.
        """

        super().__init__(f"{message} on line {ctx.start.line}")
        self.__ctx = ctx

    @property
    def ctx(self) -> ParserRuleContext:
        return self.__ctx


class UnexpectedVariableException(VisitingException):
    def __init__(self, variable_name: str, ctx: ParserRuleContext):
        super().__init__(f'Unexpected variable "{variable_name}"', ctx)


class FunctionRedefineException(VisitingException):
    def __init__(self, function_name: str, ctx: ParserRuleContext):
        super().__init__(
            f'The standard library function "{function_name}" cannot be redefined', ctx
        )


class UnknownFunctionException(VisitingException):
    def __init__(self, function_name: str, ctx: ParserRuleContext):
        super().__init__(f'Unknown function "{function_name}"', ctx)


class DuplicatedBindingException(VisitingException):
    def __init__(self, variable_name: str, ctx: ParserRuleContext):
        super().__init__(
            f'Variable "{variable_name}" appeared more than once in the bindings', ctx
        )
