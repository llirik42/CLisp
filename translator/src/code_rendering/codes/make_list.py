from typing import Any

from .code import Code


class MakeListCode(Code):
    def __init__(self, **kwargs):
        """
        Initial element count is zero and element pointer is NULL, so list is empty.
        """

        super().__init__(**kwargs)
        self.__args = [0, "NULL"]
        self.__update_args()

    def set_var(self, value: str) -> None:
        self._update_main_data(var=value)
        self._update_secondary_data(args=[value])

    def set_element_pointer(self, value: str) -> None:
        self.__args[1] = value
        self.__update_args()

    def set_element_count(self, value: int) -> None:
        self.__args[0] = value
        self.__update_args()

    def __update_args(self) -> None:
        self._update_main_data(args=self.__args)
