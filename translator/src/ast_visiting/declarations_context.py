from typing import Iterator

from src.rendering.codes import Code


class DeclarationsContext:
    """
    Class represents all declarations that must be made in generated code (function declarations, etc.).
    """

    def __init__(self):
        self.__declarations = []

    def add_declaration(self, code: Code) -> None:
        """
        Adds a declaration to the list of declarations.

        :param code: code of the declaration
        """

        self.__declarations.append(code)

    def iter_declarations(self) -> Iterator[Code]:
        """
        Returns an iterator over the declarations.
        """

        return iter(self.__declarations)
