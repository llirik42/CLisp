from typing import Optional

from .code import Code
from src.symbols import Symbols
from src.templates import Templates


class GetBooleanValueCode(Code):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            main_template=templates.GET_BOOLEAN_VALUE,
            main_data={"type": symbols.BOOLEAN_TYPE, "func": symbols.OBJECT_TO_BOOLEAN},
        )

    def update_data(self, var: Optional[str] = None, arg: Optional[str] = None) -> None:
        self._update_main_data(var=var, arg=arg)
