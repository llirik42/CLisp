__all__ = ["LambdaContext"]


# TODO: add pydoc
class LambdaContext:
    def __init__(self):
        self.__counter = 0
        self.__lambdas = {}
        self.__params = {}

    def __enter__(self):
        self.__counter += 1
        self.__params = {}

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__counter -= 1

    @property
    def inside_lambda(self) -> bool:
        return self.__counter > 0

    @property
    def params(self) -> None:
        return self.__params

    def add_param(self, lisp_name: str, c_index: int) -> None:
        self.__params[lisp_name] = c_index

    def add_lambda(self, lisp_name: str, c_var: str) -> None:
        self.__lambdas[lisp_name] = c_var

    def get_param_index(self, name: str) -> int:
        return self.__params[name]

    def get_lambda_name(self, lisp_name: str) -> str:
        return self.__lambdas[lisp_name]
