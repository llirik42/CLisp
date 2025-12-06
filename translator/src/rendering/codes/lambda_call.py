from typing import Optional

from .code import Code


class LambdaCallCode(Code):
    def __init__(self, **kwargs):
        """
        Initial args is an empty list.
        """

        super().__init__(
            required_params=["var", "lambda_var", "scalar_args_count"], **kwargs
        )

    def update_data(
        self,
        var: Optional[str] = None,
        lambda_var: Optional[str] = None,
        args: Optional[list[str]] = None,
        scalar_args_count: Optional[int] = None,
    ) -> None:
        self._update_main_data(
            var=var,
            lambda_var=lambda_var,
            args=args,
            scalar_args_count=scalar_args_count,
        )
        self._update_secondary_data(var=var)
