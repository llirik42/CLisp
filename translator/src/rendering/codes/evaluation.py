from typing import Optional

from .code import Code


class EvaluationCode(Code):
    def __init__(self, **kwargs):
        super().__init__(required_params=["var", "evaluable_var"], **kwargs)

    def update_data(
        self, var: Optional[str] = None, evaluable_var: Optional[str] = None
    ) -> None:
        self._update_main_data(var=var, evaluable_var=evaluable_var)
        self._update_secondary_data(var=var)
