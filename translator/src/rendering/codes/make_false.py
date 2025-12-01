from typing import Optional

from .code import Code


class MakeFalseCode(Code):
    def __init__(self, **kwargs):
        super().__init__(required_params=["var"], **kwargs)

    def set_var(self, var: Optional[str] = None) -> None:
        self._update_main_data(var=var)
        self._update_secondary_data(var=var)
