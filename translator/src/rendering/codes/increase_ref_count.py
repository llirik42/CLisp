from .code import Code

class IncreaseRefCountCode(Code):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_var(self, var: str) -> None:
        self._update_main_data(var=var)
