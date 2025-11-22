from .code import Code


class LambdaCallCode(Code):
    def __init__(self, **kwargs):
        """
        Initial args is an empty list.
        """

        super().__init__(**kwargs)

        self.__call_args = ["", 0, ""]
        self.__update_call_args()

    def set_var(self, value: str) -> None:
        args_var = f"{value}_args"
        self.__call_args[2] = args_var
        self._update_main_data(var=value, args_var=args_var)
        self._update_secondary_data(args=[value])

    def set_lambda(self, value: str) -> None:
        self.__call_args[0] = value
        self.__update_call_args()

    def set_args(self, value: list[str]) -> None:
        assert isinstance(value, list)

        self._update_main_data(args=value)
        self.__call_args[1] = len(value)
        self.__update_call_args()

    def __update_call_args(self) -> None:
        self._update_main_data(call_args=self.__call_args)
