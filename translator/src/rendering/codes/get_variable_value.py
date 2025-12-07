from typing import Optional

from .code import Code
from src.symbols import Symbols
from src.templates import Templates


class GetVariableValueCode(Code):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            main_template=templates.GET_VARIABLE_VALUE,
            main_data={
                "type": symbols.OBJECT_TYPE,
                "func": symbols.GET_VARIABLE_VALUE,
            },
        )

    def update_data(
        self,
        var: Optional[str] = None,
        env: Optional[str] = None,
        name: Optional[str] = None,
    ) -> None:
        self._update_main_data(var=var, env=env, name=f'"{name}"')
