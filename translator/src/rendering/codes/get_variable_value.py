from typing import Optional

from .code import Code


class GetVariableValueCode(Code):
    def __init__(self, **kwargs):
        super().__init__(required_params=["var", "env", "name"], **kwargs)

    def update_data(
        self,
        var: Optional[str] = None,
        env: Optional[str] = None,
        name: Optional[str] = None,
    ) -> None:
        self._update_main_data(var=var, env=env, name=name)
