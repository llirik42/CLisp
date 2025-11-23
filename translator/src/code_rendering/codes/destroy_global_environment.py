from typing import Optional

from .code import Code


class DestroyGlobalEnvironmentCode(Code):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_data(self, var: Optional[str] = None) -> None:
        self._update_main_data(var=var)
