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
