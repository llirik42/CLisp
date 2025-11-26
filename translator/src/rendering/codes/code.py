from abc import ABC
from typing import Optional, Any

from jinja2 import Template


def check_required(data: dict[str, Any], *args) -> None:
    for r in args:
        if r not in data:
            raise KeyError(f'"{r}" is required')


class Code(ABC):
    def __init__(
        self,
        main_template: Optional[Template] = None,
        secondary_template: Optional[Template] = None,
        main_data: Optional[dict] = None,
        secondary_data: Optional[dict] = None,
        required_params: Optional[list] = None,
    ):
        """
        Class represents a template-code that can be rendered with given data.

        The final code consists of two parts: main, secondary. For the main part there are given template, extendable epilog and newline, for the secondary there are given template and extendable prolog. Thus, the code consists of

        * main template
        * main epilog
        * \\\\n
        * secondary prolog
        * secondary template

        :param main_template: main template of code.
        :param secondary_template: template of code that will be inserted after the main one and rendered with it.
        :main_data: data that will be inserted in the main template
        :secondary_data: data that will be inserted in the secondary template
        :required_params: params that must be present in the main template
        """

        if required_params is None:
            required_params = []

        if main_data is None:
            main_data = {}

        if secondary_data is None:
            secondary_data = {}

        self.__main_data = main_data
        self.__secondary_data = secondary_data

        self.__main_epilog = ""  # Code that will be inserted after the main template
        self.__secondary_prolog = (
            ""  # Code that will be inserted before the secondary template
        )
        self.__template = main_template
        self.__secondary_template = secondary_template
        self.__is_newline_transferred = False
        self.__are_newlines_removed = False
        self.__main_validate = lambda data: check_required(data, *required_params)

    def remove_first_secondary_line(self) -> None:
        old_secondary = self.render_secondary()
        self.clear_secondary()
        new_secondary = "\n" + "\n".join(old_secondary.split("\n")[2:])
        if new_secondary[-1] == "\n":
            new_secondary = new_secondary[:-1]

        self.add_secondary_prolog(new_secondary)

    def transfer_newline(self) -> None:
        """
        Removes newline after the end of the main part and add one in the end of the secondary part. Thus, the code will consist of
        """

        self.__is_newline_transferred = True

    def remove_newlines(self) -> None:
        """
        Removes newlines between main template and main epilog, secondary prolog and secondary template. Thus, the code will consist of
        """

        self.__are_newlines_removed = True

    def add_main_epilog(self, text: str) -> None:
        """
        Adds text to the end of the main epilog.

        :param text: text to add.
        """

        self.__main_epilog += text

    def add_secondary_prolog(self, text: str) -> None:
        """
        Inserts text to the beginning of the secondary prolog.

        :param text: text to add.
        """

        self.__secondary_prolog = f"{text}{self.__secondary_prolog}"

    def render_main(self) -> str:
        """
        Renders and returns main part.
        """

        if self.__main_validate:
            self.__main_validate(self.__main_data)

        epilog = self.__main_epilog

        rendered_template = (
            self.__template.render(self.__main_data) if self.__template else ""
        )

        rendered = (
            f"{rendered_template}{epilog}"
            if self.__are_newlines_removed
            else f"{rendered_template}\n{epilog}"
        )

        if self.__is_newline_transferred:
            return rendered[:-1]  # remove trailing \n

        return rendered

    def render_secondary(self) -> str:
        """
        Renders and returns secondary part.
        """

        rendered = self.__secondary_prolog

        if self.__secondary_template:
            rendered_template = self.__secondary_template.render(self.__secondary_data)

            if self.__are_newlines_removed:
                rendered += f"{rendered_template}"
            else:
                rendered += f"\n{rendered_template}"

        if self.__is_newline_transferred:
            return f"{rendered}\n"

        return rendered

    def render(self) -> str:
        """
        Renders and returns the whole code (main + secondary).
        """

        return f"{self.render_main()}{self.render_secondary()}"

    def clear_main(self) -> None:
        """
        Removes main template and clears main epilog.
        """

        self.__main_epilog = ""
        self.__template = None

    def clear_secondary(self) -> None:
        """
        Removes secondary template and clears secondary prolog.
        """

        self.__secondary_prolog = ""
        self.__secondary_template = None

    def _update_main_data(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if v is not None:
                self.__main_data[k] = v

    def _update_secondary_data(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if v is not None:
                self.__secondary_data[k] = v
