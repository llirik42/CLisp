from typing import Optional, Union

from .code import Code
from src.symbols import Symbols
from src.templates import Templates


class MakeListFromArrayCode(Code):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            main_template=templates.MAKE_LIST_FROM_ARRAY,
            secondary_template=templates.DECREASE_REF_COUNT,
            main_data={
                "type": symbols.OBJECT_TYPE,
                "func": symbols.CREATE_LIST_FROM_ARRAY,
            },
            secondary_data={
                "func": symbols.DECREASE_REF_COUNT,
            },
        )

    def update_data(
        self,
        var: Optional[str] = None,
        count: Optional[Union[str, int]] = None,
        elements: Optional[str] = None,
    ) -> None:
        self._update_main_data(var=var, count=count, elements=elements)
        self._update_secondary_data(var=var)
