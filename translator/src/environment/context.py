from .environment import Environment
from src.code_rendering import Code
from .utils import (
    _has_variable,
    _has_variable_recursively,
    _update_variable,
    _update_variable_recursively,
)


class EnvironmentContext:
    def __init__(self):
        self.__env = None

    def init(self, name: str, code: Code):
        parent = self.__env
        self.__env = Environment(name=name, code=code, variables={}, parent=parent)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        parent = self.__env.parent
        self.__env = parent

    @property
    def code(self) -> Code:
        return self.__env.code

    @property
    def variable_count(self) -> int:
        return len(self.__env.variables)

    @property
    def name(self) -> str:
        return self.__env.name

    def has_variable(self, variable: str) -> bool:
        return _has_variable(self.__env, variable)

    def has_variable_recursively(self, name: str) -> bool:
        return _has_variable_recursively(self.__env, name)

    def update_variable(self, variable: str, value: str) -> None:
        _update_variable(self.__env, variable, value)

    def update_variable_recursively(self, variable: str, value: str) -> None:
        _update_variable_recursively(self.__env, variable, value)
