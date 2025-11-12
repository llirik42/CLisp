from antlr4 import ParserRuleContext


class VisitingException(Exception):
    def __init__(self, message: str, ctx: ParserRuleContext):
        super().__init__(f"{message} [{ctx.getText()}]")
        self.__ctx = ctx

    @property
    def ctx(self) -> ParserRuleContext:
        return self.__ctx
