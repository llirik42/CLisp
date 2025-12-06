from typing import Optional

from .code import Code


class LambdaCallCode(Code):
    def __init__(self, **kwargs):
        """
        Initial args is an empty list.
        """

        super().__init__(required_params=["var", "lambda_var"], **kwargs)

    def update_data(
        self,
        var: Optional[str] = None,
        lambda_var: Optional[str] = None,
        args: Optional[list[str]] = None,
    ) -> None:
        self._update_main_data(
            var=var,
            lambda_var=lambda_var,
            args=args,
        )
        self._update_secondary_data(var=var)
