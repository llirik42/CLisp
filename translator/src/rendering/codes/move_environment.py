from typing import Optional

from .code import Code
from src.symbols import Symbols
from src.templates import Templates


class MoveEnvironmentCode(Code):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            main_template=templates.MOVE_ENVIRONMENT,
            main_data={"func": symbols.MOVE_ENVIRONMENT},
        )

    def update_data(self, var: Optional[str] = None, env: Optional[str] = None) -> None:
        self._update_main_data(var=var, env=env)
