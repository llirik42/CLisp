from typing import Optional

from .code import Code


class ConditionCode(Code):
    def __init__(self, **kwargs):
        super().__init__(
            required_params=[
                "test_pre",
                "consequent_body",
                "alternate_body",
                "var",
                "test_after",
                "test_var",
                "consequent_var",
                "alternate_var",
            ],
            **kwargs,
        )

    def set_test_pre(self, body: str) -> None:
        self._update_main_data(test_pre=body)

    def set_test_after(self, body: str) -> None:
        self._update_main_data(test_after=body)

    def set_consequent_body(self, body: str) -> None:
        self._update_main_data(consequent_body=body)

    def set_alternate_body(self, body: str) -> None:
        self._update_main_data(alternate_body=body)

    def update_data(
        self, test_var: Optional[str] = None, var: Optional[str] = None, consequent_var: Optional[str] = None, alternate_var: Optional[str] = None
    ) -> None:
        self._update_main_data(
            test_var=test_var,
            var=var,
            consequent_var=consequent_var,
            alternate_var=alternate_var,
        )
        self._update_secondary_data(var=var)
