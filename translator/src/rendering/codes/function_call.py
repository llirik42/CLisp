from .code import Code


class FunctionCallCode(Code):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update(self, **kwargs):
        self._update_main_data(**kwargs)
