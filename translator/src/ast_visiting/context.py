class ConditionVisitingContext:
    """
    Class indicated whether visitor started visiting "condition" or not. The generated code of the visited expressions depends on this fact (while visiting "condition" procedure calls become deferred).
    """

    def __init__(self):
        self.__counter = 0  # Counter is used instead of the flag to correctly handle nested "conditions"

    def __enter__(self):
        self.__counter += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__counter -= 1

    @property
    def visiting(self):
        """
        Whether visitor started visiting "condition" or not.
        """

        return self.__counter > 0
