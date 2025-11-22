from .code import Code


class LambdaDefinition(Code):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_ret(self, value: str) -> None:
        self._update_main_data(ret=value)

    def set_body(self, value: str) -> None:
        self.__update_body(value)

    def __update_body(self, value: str) -> None:
        self._update_main_data(body=value)
