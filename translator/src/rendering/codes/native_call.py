from typing import Optional

from .code import Code
from src.symbols import Symbols
from src.templates import Templates


class NativeCallCode(Code):
    def __init__(self, symbols: Symbols, templates: Templates):
        super().__init__(
            main_template=templates.NATIVE_CALL,
            secondary_template=templates.DECREASE_REF_COUNT,
            main_data={
                "type": symbols.OBJECT_TYPE,
                "arg_type": symbols.NATIVE_ARGUMENT_TYPE,
                "calling_func": symbols.NATIVE_CALL,
            },
            secondary_data={
                "func": symbols.DECREASE_REF_COUNT,
            },
        )

    def update_data(
        self,
        var: Optional[str] = None,
        function: Optional[str] = None,
        library: Optional[str] = None,
        result_type: Optional[str] = None,
        args_types: Optional[list[str]] = None,
    ) -> None:
        if args_types is None:
            args_types = []

        self._update_main_data(
            var=var,
            function=f'"{function}"',
            library=f'"{library}"',
            result_type=result_type,
            args_types=args_types,
        )
        self._update_secondary_data(var=var)
