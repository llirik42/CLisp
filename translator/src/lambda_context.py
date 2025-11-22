__all__ = ["LambdaContext"]

from src.code_rendering import Code


# TODO: add pydoc
class LambdaContext:
    def __init__(self):
        self.__counter = 0
        self.__lambdas = {}
        self.__params = {}
        self.__code = None

    def __enter__(self):
        self.__counter += 1
        self.__params = {}

    def set_code(self, code: Code) -> None:
        self.__code = code

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__counter -= 1

    @property
    def code(self) -> Code:
        assert self.__code is not None
        return self.__code

    @property
    def inside_lambda(self) -> bool:
        return self.__counter > 0

    @property
    def params(self) -> None:
        return self.__params

    def add_param(self, lisp_name: str, c_name: str, variadic: bool = False) -> None:
        self.__params[lisp_name] = (c_name, variadic)

    def add_lambda(self, lisp_name: str, c_var: str) -> None:
        self.__lambdas[lisp_name] = c_var

    def get_param_index(self, name: str) -> int:
        return self.__params[name]

    def get_lambda_name(self, lisp_name: str) -> str:
        return self.__lambdas[lisp_name]

    def get_param_c_name(self, lisp_name: str) -> str:
        return self.__params[lisp_name]
