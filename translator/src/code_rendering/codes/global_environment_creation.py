from typing import Optional

from .code import Code


class GlobalEnvironmentCreation(Code):
    def __init__(self, **kwargs):
        """
        Initial body is empty.
        """

        super().__init__(**kwargs)
        self._update_main_data(body="")

    def update_data(
        self,
        func: Optional[str] = None,
        var: Optional[str] = None,
    ) -> None:
        self._update_main_data(func=func, var=var)

    def add_to_body(self, delta: str, newline: bool = True) -> None:
        old = self._get_main_data("body")
        new = old + delta
        if newline:
            new += "\n"
        self._update_main_data(body=new)
