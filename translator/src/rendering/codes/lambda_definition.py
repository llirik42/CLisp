from typing import Optional

from .code import Code


class LambdaDefinitionCode(Code):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_data(
        self,
        body: Optional[str] = None,
        ret_var: Optional[str] = None,
        func: Optional[str] = None,
    ) -> None:
        self._update_main_data(body=body, ret_var=ret_var, func=func)
