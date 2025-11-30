from .code import Code

class MakeUnspecifiedCode(Code):
    def __init__(self, **kwargs):
        super().__init__(required_params=["var"], **kwargs)

    def update_data(self, var: str) -> None:
        self._update_main_data(var=var)
        self._update_secondary_data(var=var)
