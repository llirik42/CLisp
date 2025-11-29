class LambdaContext:
    """
    The class represents information about the currently visiting lambda function.
    """

    def __init__(self):
        self.__counter = 0
        self.__params = {}

    def __enter__(self):
        self.__counter += 1
        self.__params = {}

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__counter -= 1

    @property
    def inside_lambda(self) -> bool:
        """
        Whether a lambda is being visited or not.
        """
        return self.__counter > 0

    def set_param_var(self, param_name: str, param_var: str) -> None:
        """
        Adds a parameter to the current lambda.

        :param param_name: name of the parameter (in `(lambda (x y) ...)` it could be "x" or "y")
        :param param_var: variable in which the parameter value is stored (like `var1`, `var2`, ...)
        """

        self.__params[param_name] = param_var

    def get_param_var(self, param_name: str) -> str:
        """
        Returns parameter's variable in the current lambda.

        :param param_name: name of the parameter
        :raises KeyError: current lambda doesn't have parameter with given name
        """

        return self.__params[param_name]

    def has_param(self, param_name: str) -> bool:
        """
        Whether a parameter exists in the current lambda.
        """

        return self.__params.get(param_name, None) is not None

    @property
    def params(self):
        return self.__params
