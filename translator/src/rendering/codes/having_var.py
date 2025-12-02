from typing import Optional

from .code import Code


class HavingVarCode(Code):
    def __init__(self, **kwargs):
        if "required_params" in kwargs:
            kwargs["required_params"].append("var")
        else:
            kwargs["required_params"] = ["var"]
        super().__init__(**kwargs)

    def update_data(self, var: Optional[str] = None) -> None:
        self._update_main_data(var=var)
        self._update_secondary_data(var=var)
