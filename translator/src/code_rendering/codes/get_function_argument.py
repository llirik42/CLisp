from .code import Code


class GetFunctionArgumentCode(Code):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_var(self, value: str) -> None:
        self._update_main_data(var=value)

    def set_array(self, value: str) -> None:
        self._update_main_data(array=value)

    def set_index(self, value: int) -> None:
        self._update_main_data(index=value)
