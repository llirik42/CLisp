from typing import Any

from .code import Code


class MakeLambdaCode(Code):
    def __init__(self, **kwargs):
        """
        Initial environment is NULL


        """

        super().__init__(**kwargs)
        self.__args = ["", "NULL"]
        self.__update_args()

    def set_var(self, value: str) -> None:
        self._update_main_data(var=value)
        self._update_secondary_data(args=[value])

    def set_func(self, value: str) -> None:
        self.__args[0] = value
        self.__update_args()

    def set_env(self, value: str) -> None:
        self.__args[1] = value
        self.__update_args()

    def __update_args(self) -> None:
        self._update_main_data(args=self.__args)
