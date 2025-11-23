from typing import Optional

from .code import Code


class GlobalEnvironmentDestroying(Code):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._update_main_data(body="")

    def update_data(
        self,
        func: Optional[str] = None,
        var: Optional[str] = None,
    ) -> None:
        self._update_main_data(func=func, var=var)

    def add_to_body(self, delta: str) -> None:
        old = self._get_main_data("body")
        self._update_main_data(body=old + delta)
