from src.code_rendering import Code
from dataclasses import dataclass



@dataclass()
class Environment:
    name: str
    code: Code
    variables: dict[str, str]
    parent: "Environment"

    @property
    def has_parent(self) -> bool:
        return self.parent is not None


def has_variable(env: Environment, variable: str) -> bool:
    return variable in env.variables

def has_variable_recursively(env: Environment, name: str) -> bool:
    if has_variable(env, name):
        return True

    if env.has_parent:
        return has_variable_recursively(env.parent, name)

    return False

def update_variable(env: Environment, variable: str, value: str) -> None:
    env.variables[variable] = value

def update_variable_recursively(env: Environment, variable: str, value: str) -> None:
    if variable in env.variables:
        env.variables[variable] = value

    if env.has_parent:
        update_variable_recursively(env.parent, variable, value)




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
        return has_variable(self.__env, variable)

    def has_variable_recursively(self, name: str) -> bool:
        return has_variable_recursively(self.__env, name)

    def update_variable(self, variable: str, value: str) -> None:
        update_variable(self.__env, variable, value)

    def update_variable_recursively(self, variable: str, value: str) -> None:
        update_variable_recursively(self.__env, variable, value)
