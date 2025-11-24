from src.code_rendering import Code
from .environment import Environment


class EnvironmentContext:
    """
    Class represents context with all environments during code-generating. This class is a context-manager, so it should be used like this:

    **Example**

        ctx = EnvironmentContext()
        with ctx:
            ctx.init(name=..., code=...)  # New environment creation
            # Some code that works with the first environment
            ...

            with ctx:
                ctx.init(name=..., code=...)  # New environment creation
                # Some code that works with the second environment
                ...

            # Some code that works again with the first environment
            ...

        # There is no environment here
    """

    def __init__(self):
        self.__env = None

    def init(self, name: str, code: Code):
        """
        Creates new environment with given name and code, sets current environment to new one and remembers previous one as parent.

        :param name: name of the environment
        :param code: code of the environment
        """

        parent = self.__env
        self.__env = Environment(name=name, code=code, variables={}, parent=parent)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Resets current environment to the parent one.
        """

        parent = self.__env.parent
        self.__env = parent

    @property
    def code(self) -> Code:
        """
        Code of the current environment.
        """

        return self.__env.code

    @property
    def variable_count(self) -> int:
        """
        Count of the variables in the current environment.
        """

        return len(self.__env.variables)

    @property
    def name(self) -> str:
        """
        Name of the current environment.
        """

        return self.__env.name

    def has_variable(self, variable: str) -> bool:
        """
        Whether current environment has the given variable.

        :param variable: name of the variable to check
        """

        return self.__env.has_variable(variable)

    def has_variable_recursively(self, variable: str) -> bool:
        """
        Whether current environment has the given variable in it ancestral tree (current -> parent -> parent of the parent -> etc).

        :param variable: name of the variable to check
        """

        return self.__env.has_variable_recursively(variable)

    def update_variable(self, variable: str, value: str) -> None:
        """
        Sets variable value in the current environment.

        :param variable: name of the variable
        :param value: value of the variable
        """

        self.__env.update_variable(variable, value)

    def update_variable_recursively(self, variable: str, value: str) -> None:
        """
        Sets variable in the current environment or the first ancestral that has the variable.

        :param variable: name of the variable
        :param value: value of the variable
        """

        self.__env.update_variable_recursively(variable, value)

    @property
    def env(self) -> Environment:
        return self.__env
