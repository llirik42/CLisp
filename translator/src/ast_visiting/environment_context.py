from src.rendering.codes import Code
from src.environment import Environment


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
        self.__env = Environment(
            name=name, code=code, parent=parent
        )

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Resets current environment to the parent one.
        """

        parent = self.__env.parent
        self.__env = parent

    @property
    def env(self) -> Environment:
        """
        Current environment.

        :raises Exception: there are no active environment
        """

        if self.__env is None:
            raise Exception("No active environment")

        return self.__env
