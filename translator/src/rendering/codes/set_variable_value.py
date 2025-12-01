from typing import Optional

from .code import Code


class SetVariableValueCode(Code):
    def __init__(self, **kwargs):
        super().__init__(required_params=["env", "name", "value", "auto_remove"], **kwargs)

    def update_data(
        self,
        env: Optional[str] = None,
        name: Optional[str] = None,
        value: Optional[str] = None,
        auto_remove: int = 1,
    ) -> None:
        self._update_main_data(env=env, name=f'"{name}"', value=value, auto_remove=auto_remove)
