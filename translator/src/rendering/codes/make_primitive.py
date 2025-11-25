from typing import Union, Optional

from .code import Code


class MakePrimitiveCode(Code):
    def __init__(self, **kwargs):
        super().__init__(required_params=["var", "value"], **kwargs)

    def update_data(
        self, var: Optional[str] = None, value: Optional[Union[str, int, float]] = None
    ) -> None:
        self._update_main_data(var=var, value=value)
        self._update_secondary_data(var=var)
