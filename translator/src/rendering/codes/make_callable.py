from typing import Optional

from .code import Code
from src.symbols import Symbols
from src.templates import Templates


class MakeCallableCode(Code):
    def __init__(self, symbols: Symbols, templates: Templates, func: str):
        super().__init__(
            main_template=templates.MAKE_CALLABLE,
            secondary_template=templates.DECREASE_REF_COUNT,
            main_data={
                "type": symbols.OBJECT_TYPE,
                "creation_func": func,
            },
            secondary_data={"func": symbols.DECREASE_REF_COUNT},
        )

    def update_data(
        self,
        var: Optional[str] = None,
        func: Optional[str] = None,
        env: Optional[str] = None,
    ) -> None:
        self._update_main_data(var=var, func=func, env=env)
        self._update_secondary_data(var=var)


class MakeLambdaCode(MakeCallableCode):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            symbols=symbols, templates=templates, func=symbols.CREATE_LAMBDA
        )


class MakeEvaluableCode(MakeCallableCode):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            symbols=symbols, templates=templates, func=symbols.CREATE_EVALUABLE
        )
