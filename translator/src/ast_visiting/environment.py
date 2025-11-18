from src.code_rendering import Code


class Environment:
    def __init__(self, code: Code, name: str):
        self.__code = code
        self.__name = name
        self.__parent: Environment
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

    def update_variable(self, lisp_name: str, c_name) -> None:
        self.__variables[lisp_name] = c_name
