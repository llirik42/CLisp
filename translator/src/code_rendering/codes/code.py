from typing import Optional, Callable, Any

from jinja2 import Template
from abc import ABC


class Code(ABC):
    def __init__(
        self,
        main_template: Optional[Template] = None,
        secondary_template: Optional[Template] = None,
        main_data: Optional[dict] = None,
        secondary_data: Optional[dict] = None,
        main_validate: Optional[Callable[[dict], None]] = None,
        secondary_validate: Optional[Callable[[dict], None]] = None,
        empty: bool = False,
        **kwargs,
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
        :param kwargs: initial data.
        """

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
        self.__final = False
        self.__final_final = False
        self.__main_validate = main_validate
        self.__secondary_validate = secondary_validate
        self.__empty = empty

    @property
    def final(self) -> bool:
        return self.__final

    def make_final(self) -> None:
        """
        Makes the code "final". Being "final" means that there will be no newline in the end of the main part and will be additional newline in the end of the secondary part. Thus, the code will consist of

        * main template
        * main epilog
        * secondary prolog
        * secondary template
        * \\\\n
        """

        self.__final = True

    def make_final_final(self) -> None:
        self.__final_final = True

    # def update_data(self, **kwargs) -> None:
    #     """
    #     Update data that will be used for rendering.
    #
    #     :param kwargs: data to update.
    #     """
    #
    #     self.__common_data.update(kwargs)

    def add_main_epilog(self, text: str):
        """
        Adds text to the end of the main epilog.

        :param text: text to add.
        """

        self.__main_epilog += text

    def add_secondary_prolog(self, text: str):
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

        result = self.__main_epilog

        tmp = ""
        if self.__template:
            tmp = self.__template.render(self.__main_data)

        if self.__final_final:
            rendered = f"{tmp}{result}"
        else:
            rendered = f"{tmp}\n{result}"

        if self.__final:
            return rendered[:-1]  # remove trailing \n

        return rendered

    def render_secondary(self) -> str:
        """
        Renders and returns secondary part.
        """

        if self.__secondary_validate:
            self.__secondary_validate(self.__secondary_data)

        rendered = self.__secondary_prolog

        if self.__secondary_template:
            if self.__final_final:
                rendered += f"{self.__secondary_template.render(self.__secondary_data)}"
            else:
                rendered += (
                    f"\n{self.__secondary_template.render(self.__secondary_data)}"
                )

        if self.__final:
            return f"{rendered}\n"

        return rendered

    def render(self) -> str:
        """
        Renders and returns the whole code (main + secondary).
        """

        return f"{self.render_main()}{self.render_secondary()}"

    def clear_main(self) -> None:
        self.__main_epilog = ""
        self.__template = None

    def clear_secondary(self) -> None:
        """
        Completely cleanses the secondary part (template + prolog).
        """

        self.__secondary_prolog = ""
        self.__secondary_template = None

    @property
    def is_empty(self) -> bool:
        return self.__empty

    def get_main_data(self, key: str) -> Any:
        return self.__main_data.get(key, None)

    def get_main_secondary(self, key: str) -> Any:
        return self.__secondary_data.get(key, None)

    def _update_main_data(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if v is not None:
                self.__main_data[k] = v

    def _update_secondary_data(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if v is not None:
                self.__secondary_data[k] = v
