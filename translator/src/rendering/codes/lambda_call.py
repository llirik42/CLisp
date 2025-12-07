from typing import Optional

from .code import Code
from src.symbols import Symbols
from src.templates import Templates


class LambdaCallCode(Code):
    def __init__(self, symbols: Symbols, templates: Templates, func: str):
        super().__init__(
            main_template=templates.LAMBDA_CALL,
            secondary_template=templates.DECREASE_REF_COUNT,
            main_data={
                "type": symbols.OBJECT_TYPE,
                "args_type": symbols.OBJECT_TYPE,
                "func": func,
            },
            secondary_data={
                "func": symbols.DECREASE_REF_COUNT,
            },
        )

    def update_data(
        self,
        var: Optional[str] = None,
        lambda_var: Optional[str] = None,
        args: Optional[list[str]] = None,
    ) -> None:
        self._update_main_data(
            var=var,
            lambda_var=lambda_var,
            args=args,
        )
        self._update_secondary_data(var=var)


class OrdinaryLambdaCallCode(LambdaCallCode):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(symbols=symbols, templates=templates, func=symbols.CALL_LAMBDA)


class ListLambdaCallCode(LambdaCallCode):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            symbols=symbols, templates=templates, func=symbols.CALL_LAMBDA_LIST
        )
