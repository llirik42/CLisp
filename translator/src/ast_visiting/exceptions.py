from antlr4 import ParserRuleContext


class VisitingException(Exception):
    def __init__(self, message: str, ctx: ParserRuleContext):
        """
        Class represents an exception that can be thrown during visiting of AST.

        :param message: message.
        :param ctx: context of the visiting.
        """

        super().__init__(f"{message} on lines {ctx.start.line}-{ctx.stop.line}")
        self.__ctx = ctx

    @property
    def ctx(self) -> ParserRuleContext:
        return self.__ctx


class UnexpectedIdentifierException(VisitingException):
    def __init__(self, identifier: str, ctx: ParserRuleContext):
        super().__init__(f'Unexpected identifier "{identifier}"', ctx)


class FunctionRedefineException(VisitingException):
    def __init__(self, function_name: str, ctx: ParserRuleContext):
        super().__init__(
            f'The standard library function "{function_name}" cannot be redefined', ctx
        )
