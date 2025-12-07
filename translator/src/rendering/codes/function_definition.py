from typing import Optional

from .code import Code
from src.symbols import Symbols
from src.templates import Templates


class FunctionDefinitionCode(Code):
    def __init__(self, symbols: Symbols, templates: Templates, params: str):
        super().__init__(
            main_template=templates.FUNCTION_DEFINITION,
            main_data={
                "ret_type": symbols.OBJECT_TYPE,
                "params": params,
            },
        )

    def update_data(
        self,
        body: Optional[str] = None,
        ret_var: Optional[str] = None,
        func: Optional[str] = None,
    ) -> None:
        self._update_main_data(body=body, ret_var=ret_var, func=func)


class LambdaDefinition(FunctionDefinitionCode):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            symbols=symbols, templates=templates, params=symbols.LAMBDA_PARAMS
        )


class EvaluableDefinition(FunctionDefinitionCode):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            symbols=symbols, templates=templates, params=symbols.EVALUABLE_PARAMS
        )
