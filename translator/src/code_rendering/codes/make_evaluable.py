from typing import Optional

from .code import Code


class MakeEvaluableCode(Code):
    def __init__(self, **kwargs):
        """
        Initial args is an empty list.
        """

        super().__init__(**kwargs)

    def update_data(
        self,
        var: Optional[str] = None,
        func: Optional[str] = None,
        args: Optional[list[str]] = None,
    ) -> None:
        self._update_main_data(var=var, func=func, args=args)
        self._update_secondary_data(var=var)
