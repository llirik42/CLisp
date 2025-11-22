from .code import Code


class UpdateVariableValueCode(Code):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__args = ["", "", ""]
        self.__update_args()

    def set_var(self, value: str) -> None:
        self._update_main_data(var=value)
        self._update_secondary_data(args=[value])

    def set_value(self, value: str) -> None:
        self.__args[2] = value
        self.__update_args()

    def set_env(self, value: str) -> None:
        self.__args[0] = value
        self.__update_args()

    def set_name(self, value: str) -> None:
        self.__args[1] = value
        self.__update_args()

    def __update_args(self) -> None:
        self._update_main_data(args=self.__args)
