from typing import Optional

from .code import Code
from src.symbols import Symbols
from src.templates import Templates


class MakeFalseCode(Code):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            main_template=templates.MAKE_PRIMITIVE,
            secondary_template=templates.DECREASE_REF_COUNT,
            main_data={
                "type": symbols.OBJECT_TYPE,
                "func": symbols.CREATE_FALSE,
            },
            secondary_data={
                "func": symbols.DECREASE_REF_COUNT,
            },
        )

    def update_data(self, var: Optional[str] = None) -> None:
        self._update_main_data(var=var)
        self._update_secondary_data(var=var)
