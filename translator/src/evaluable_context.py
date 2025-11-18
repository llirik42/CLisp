__all__ = ["EvaluableContext"]


class EvaluableContext:
    """
    Class indicates whether "evaluable objects" should be made instead of a regular function call or not. For example, while visiting an expression "condition" procedure calls become deferred. It means that generated code should contain not a regular procedure call, but an "evaluable object" which will be the wrapper for the procedure call.
    """

    def __init__(self):
        # Counter is used instead of the flag to correctly handle nested expressions ("condition", "and", "or")
        self.__counter = 0

    def __enter__(self):
        self.__counter += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__counter -= 1

    @property
    def should_make_evaluable(self) -> bool:
        """
        Whether should "evaluable" be made instead of a regular function call or not.
        """

        return self.__counter > 0
