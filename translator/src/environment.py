from src.rendering.codes import Code


__all__ = ["Environment"]


class Environment:
    """
    Class represents a variable environment: list of the defined Lisp-variables.
    """

    def __init__(self, name: str, code: Code, parent: "Environment", is_global: bool):
        self.__name = name
        self.__code = code
        self.__variables = set()
        self.__parent = parent
        self.__is_global = is_global

    @property
    def has_parent(self) -> bool:
        """
        Returns whether this environment has a parent one.
        """

        return self.__parent is not None

    @property
    def is_global(self) -> bool:
        """
        Returns whether this environment is a global one.
        """

        return self.__is_global

    def has_variable(self, variable: str) -> bool:
        """
        Returns whether this environment has a variable.
        """

        return variable in self.__variables

    def has_variable_recursively(self, name: str) -> bool:
        """
        Returns whether this environment or any of its ancestors has a variable.
        """

        if self.has_variable(name):
            return True

        if self.has_parent:
            return self.__parent.has_variable_recursively(name)

        return False

    def add_variable(self, name: str) -> None:
        """
        Adds a variable to the environment.

        :param name: the name of the variable.
        """

        self.__variables.add(name)

    @property
    def name(self) -> str:
        """
        Name of the environment.
        """

        return self.__name

    @property
    def code(self) -> Code:
        """
        Code of the environment.
        """

        return self.__code

    @property
    def parent(self) -> "Environment":
        """
        Parent of the environment.
        """

        return self.__parent
