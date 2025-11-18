from src.code_rendering import Code


class Environment:
    def __init__(self, code: Code, name: str, parent=None):
        self.__code = code
        self.__name = name
        self.__parent = parent
        self.__variables = {}

    @property
    def code(self) -> Code:
        return self.__code

    @property
    def variable_count(self) -> int:
        return len(self.__variables)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def parent(self):
        return self.__parent

    def has_variable(self, variable: str) -> bool:
        return variable in self.__variables

    def has_variable_recursively(self, name: str) -> bool:
        if self.has_variable(name):
            return True

        if self.__has_parent:
            return self.__parent.has_variable_recursively(name)

        return False

    def update_variable(self, variable: str, value: str) -> None:
        self.__variables[variable] = value

    def update_variable_recursively(self, variable: str, value: str) -> None:
        if variable in self.__variables:
            self.__variables[variable] = value
            return

        if self.__has_parent:
            self.__parent.update_variable_recursively(variable, value)

    @property
    def __has_parent(self) -> bool:
        return self.__parent is not None


class EnvironmentContext:
    def __init__(self):
        self.__environment = None

    def init(self, code: Code, name: str):
        current_env = self.__env
        new_env = Environment(code=code, name=name, parent=current_env)
        self.__env = new_env

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        parent = self.__env.parent
        self.__env = parent

    @property
    def code(self) -> Code:
        return self.__code

    @property
    def variable_count(self) -> int:
        return len(self.__variables)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def parent(self):
        return self.__parent

    def has_variable(self, variable: str) -> bool:
        return variable in self.__variables

    def has_variable_recursively(self, name: str) -> bool:
        if self.has_variable(name):
            return True

        if self.__has_parent:
            return self.__parent.has_variable_recursively(name)

        return False

    def update_variable(self, variable: str, value: str) -> None:
        self.__variables[variable] = value

    def update_variable_recursively(self, variable: str, value: str) -> None:
        if variable in self.__variables:
            self.__variables[variable] = value
            return

        if self.__has_parent:
            self.__parent.update_variable_recursively(variable, value)

    @property
    def __has_parent(self) -> bool:
        return self.__parent is not None
