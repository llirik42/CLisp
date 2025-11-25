from typing import Optional

from .code import Code


class GetFunctionArgumentCode(Code):
    def __init__(self, **kwargs):
        super().__init__(required_params=["var", "index"], **kwargs)

    def update_data(
        self, var: Optional[str] = None, index: Optional[int] = None
    ) -> None:
        self._update_main_data(var=var, index=index)
