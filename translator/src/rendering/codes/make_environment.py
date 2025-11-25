from typing import Optional

from .code import Code


class MakeEnvironmentCode(Code):
    def __init__(self, **kwargs):
        """
        Initial capacity is zero, and initial parent in NULL
        """

        super().__init__(**kwargs)
        self._update_main_data(parent="NULL")

    def update_data(
        self, var: Optional[str] = None, parent: Optional[str] = None
    ) -> None:
        self._update_main_data(var=var, parent=parent)
        self._update_secondary_data(var=var)
