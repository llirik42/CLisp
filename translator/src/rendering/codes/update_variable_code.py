from typing import Optional

from .code import Code
from src.symbols import Symbols
from src.templates import Templates


class UpdateVariableValueCode(Code):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            main_template=templates.UPDATE_VARIABLE_VALUE,
            secondary_template=templates.DECREASE_REF_COUNT,
            main_data={
                "type": symbols.OBJECT_TYPE,
                "func": symbols.UPDATE_VARIABLE_VALUE,
            },
            secondary_data={
                "func": symbols.DECREASE_REF_COUNT,
            },
        )

    def update_data(
        self,
        var: Optional[str] = None,
        env: Optional[str] = None,
        name: Optional[str] = None,
        value: Optional[str] = None,
    ) -> None:
        self._update_main_data(var=var, env=env, name=f'"{name}"', value=value)
        self._update_secondary_data(var=var)
