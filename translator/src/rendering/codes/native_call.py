from typing import Optional

from .code import Code


class NativeCallCode(Code):
    def __init__(self, **kwargs):
        super().__init__(
            required_params=["var", "library", "function", "result_type"], **kwargs
        )

    def update_data(
        self,
        var: Optional[str] = None,
        function: Optional[str] = None,
        library: Optional[str] = None,
        result_type: Optional[str] = None,
        args_types: list[str] = None,
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
