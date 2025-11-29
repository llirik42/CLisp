from typing import Optional

from .code import Code


class ProgramCode(Code):
    def __init__(self, **kwargs):
        """
        Initial body of the main is empty and there are no declarations.
        """

        super().__init__(**kwargs)
        self._update_main_data(main_body="")

    def update_data(
        self,
        main_body: Optional[str] = None,
        declarations: Optional[list[str]] = None,
    ) -> None:
        self._update_main_data(
            main_body=main_body,
            declarations=declarations,
        )
