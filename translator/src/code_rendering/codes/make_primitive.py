from typing import Union

from .code import Code


class MakePrimitiveCode(Code):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_var(self, value: str) -> None:
        self._update_main_data(var=value)
        self._update_secondary_data(args=[value])

    def set_value(self, value: Union[int, str, float]) -> None:
        self._update_main_data(args=[value])
