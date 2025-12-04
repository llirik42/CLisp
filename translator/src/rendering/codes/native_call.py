from typing import Optional

from .code import Code


class NativeCallCode(Code):
    def __init__(self, **kwargs):
        super().__init__(
            required_params=["var", "library", "func", "result_type"], **kwargs
        )

    def update_data(
        self,
        var: Optional[str] = None,
        func: Optional[str] = None,
        library: Optional[str] = None,
        result_type: Optional[str] = None,
        args: list[tuple[str, str]] = None,
    ) -> None:
        if args is None:
            args = []

        self._update_main_data(
            var=var,
            func=f'"{func}"',
            library=f'"{library}"',
            result_type=result_type,
            args=args,
        )
        self._update_secondary_data(var=var)
