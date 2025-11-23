from typing import Optional

from .code import Code


class MakeLambdaCode(Code):
    def __init__(self, **kwargs):
        """
        Initial environment is NULL.
        """

        super().__init__(**kwargs)
        self._update_main_data(env="NULL")

    def update_data(
        self,
        var: Optional[str] = None,
        func: Optional[str] = None,
        env: Optional[str] = None,
    ) -> None:
        self._update_main_data(var=var, func=func, env=env)
        self._update_secondary_data(var=var)
