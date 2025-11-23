from typing import Optional

from .code import Code


class MakeListCode(Code):
    def __init__(self, **kwargs):
        """
        Initial element count is zero and element pointer is NULL (the list will be empty).
        """

        super().__init__(**kwargs)
        self._update_main_data(count=0, elements="NULL")

    def update_data(
        self,
        var: Optional[str] = None,
        count: Optional[int] = None,
        elements: Optional[str] = None,
    ) -> None:
        self._update_main_data(var=var, count=count, elements=elements)
        self._update_secondary_data(var=var)
