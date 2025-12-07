from typing import Union, Optional

from .code import Code
from src.symbols import Symbols
from src.templates import Templates


class MakePrimitiveCode(Code):
    def __init__(self, symbols: Symbols, templates: Templates, func: str):
        super().__init__(
            main_template=templates.MAKE_PRIMITIVE,
            secondary_template=templates.DECREASE_REF_COUNT,
            main_data={
                "type": symbols.OBJECT_TYPE,
                "func": func,
            },
            secondary_data={
                "func": symbols.DECREASE_REF_COUNT,
            },
        )

    def update_data(
        self, var: Optional[str] = None, value: Optional[Union[str, int, float]] = None
    ) -> None:
        self._update_main_data(var=var, value=value)
        self._update_secondary_data(var=var)


class MakeIntCode(MakePrimitiveCode):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            symbols=symbols, templates=templates, func=symbols.CREATE_INTEGER
        )


class MakeFloatCode(MakePrimitiveCode):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            symbols=symbols, templates=templates, func=symbols.CREATE_FLOAT
        )


class MakeStringCode(MakePrimitiveCode):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            symbols=symbols, templates=templates, func=symbols.CREATE_STRING
        )


class MakeCharacterCode(MakePrimitiveCode):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            symbols=symbols, templates=templates, func=symbols.CREATE_CHARACTER
        )
