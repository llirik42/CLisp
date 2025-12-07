from typing import Optional

from .code import Code
from src.symbols import Symbols
from src.templates import Templates


class SetVariableValueCode(Code):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            main_template=templates.SET_VARIABLE_VALUE,
            main_data={
                "type": symbols.OBJECT_TYPE,
                "func": symbols.SET_VARIABLE_VALUE,
            },
        )

    def update_data(
        self,
        env: Optional[str] = None,
        name: Optional[str] = None,
        value: Optional[str] = None,
    ) -> None:
        self._update_main_data(env=env, name=f'"{name}"', value=value)
