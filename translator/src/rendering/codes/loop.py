from typing import Optional

from .code import Code


class LoopCode(Code):
    def __init__(self, **kwargs):
        super().__init__(
            required_params=[
                "var",
                "pre_body",
                "post_body",
                "test_body",
                "test_value",
                "true_test_body",
                "true_test_var",
                "false_test_body",
            ],
            **kwargs,
        )

    def update_data(
        self,
        var: Optional[str] = None,
        pre_body: Optional[str] = None,
        post_body: Optional[str] = None,
        test_body: Optional[str] = None,
        test_value: Optional[str] = None,
        true_test_body: Optional[str] = None,
        true_test_var: Optional[str] = None,
        false_test_body: Optional[str] = None,
    ) -> None:
        self._update_main_data(
            var=var,
            pre_body=pre_body,
            post_body=post_body,
            test_body=test_body,
            test_value=test_value,
            true_test_body=true_test_body,
            true_test_var=true_test_var,
            false_test_body=false_test_body,
        )
        self._update_secondary_data(var=var)
