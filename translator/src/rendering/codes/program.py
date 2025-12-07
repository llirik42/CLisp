from typing import Optional

from .code import Code
from src.symbols import Symbols
from src.templates import Templates


class ProgramCode(Code):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            main_template=templates.PROGRAM,
        )

    def update_data(
        self,
        main_body: Optional[str] = None,
        declarations: Optional[list[str]] = None,
    ) -> None:
        self._update_main_data(
            main_body=main_body,
            declarations=declarations,
        )
