from typing import Optional

from .code import Code
from src.symbols import Symbols
from src.templates import Templates


class ConditionCode(Code):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            main_template=templates.IF,
            secondary_template=templates.DECREASE_REF_COUNT,
            main_data={"type": symbols.OBJECT_TYPE, "func": symbols.OBJECT_TO_BOOLEAN},
            secondary_data={"func": symbols.DECREASE_REF_COUNT},
        )

    def update_data(
        self,
        var: Optional[str] = None,
        cond_var: Optional[str] = None,
        then_var: Optional[str] = None,
        else_var: Optional[str] = None,
        then_body: Optional[str] = None,
        else_body: Optional[str] = None,
        pre_body: Optional[str] = None,
        post_body: Optional[str] = None,
    ) -> None:
        self._update_main_data(
            var=var,
            cond_var=cond_var,
            then_var=then_var,
            else_var=else_var,
            then_body=then_body,
            else_body=else_body,
            pre_body=pre_body,
            post_body=post_body,
        )
        self._update_secondary_data(var=var)
