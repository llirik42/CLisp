from enum import StrEnum, auto


class LetType(StrEnum):
    LET = (auto(),)
    LET_REC = (auto(),)
    LET_ASTERISK = (auto(),)


class LetTypeContext:
    """
    Class represents type of the currently visiting let-construction: let, let* or letrec.
    """

    def __init__(self):
        self.__types = []

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__types.pop()

    def visit(self, type_: LetType) -> None:
        """
        Sets type of the current let-construction.
        """

        self.__types.append(type_)

    @property
    def type_(self):
        """
        Type of the current let-construction.
        """

        return self.__types[-1]
