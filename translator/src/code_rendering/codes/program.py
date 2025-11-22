from .code import Code


class ProgramCode(Code):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__update_main_body("")

    def set_main_body(self, value: str) -> None:
        self.__update_main_body(value)

    def set_declarations(self, value: list[str]) -> None:
        self._update_main_data(declarations=value)

    def __update_main_body(self, value) -> None:
        self._update_main_data(main_body=value)
