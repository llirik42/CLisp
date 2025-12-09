from antlr4 import ParserRuleContext


class VisitingException(Exception):
    def __init__(self, message: str, ctx: ParserRuleContext):
        """
        Class represents an exception that can be thrown during visiting of AST.

        :param message: message.
        :param ctx: context of the visiting.
        """

        shift = 59  # From preprocessing

        start = ctx.start.line - shift
        stop =  ctx.stop.line - shift

        if start == stop:
            arg = f"{message} on line {start}"
        else:
            arg = f"{message} on lines {start}-{stop}"
        
        super().__init__(arg)
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
