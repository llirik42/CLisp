from antlr4 import ParserRuleContext


class ASTContext:
    """
    Class represents an information about current visiting AST node.
    """

    def __init__(self):
        self.__contexts = []

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__contexts.pop()

    def visit(self, ctx: ParserRuleContext) -> None:
        """
        Sets given AST node context as current.

        :param ctx: AST node context
        """

        self.__contexts.append(ctx)

    @property
    def ctx(self) -> ParserRuleContext:
        """
        Current AST node context.
        """

        return self.__contexts[-1]


def visit(context: ASTContext):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            with context:
                antlr4_ctx = args[-1]
                context.visit(antlr4_ctx)
                return method(self, *args, **kwargs)

        return wrapper

    return decorator
