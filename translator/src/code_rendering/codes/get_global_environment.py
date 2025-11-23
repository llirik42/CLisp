from typing import Optional

from .code import Code


class GetGlobalEnvironmentCode(Code):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_data(
        self,
        var: Optional[str] = None,
        get_func: Optional[str] = None,
        destroy_func: Optional[str] = None,
    ) -> None:
        self._update_main_data(var=var, func=get_func)
        self._update_secondary_data(var=var, func=destroy_func)
