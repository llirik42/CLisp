from typing import Optional

from jinja2 import Template


class Code:
    def __init__(
        self,
        template: Template,
        secondary_template: Optional[Template] = None,
        **kwargs,
    ):
        """
        Class represents a template-code that can be rendered with given data.

        The final code consists of two parts: main, secondary. For the main part there are given template and extendable epilog, for the secondary there are given template and extendable prolog. Thus, the code consists of

        * main template
        * main epilog
        * \\\\n
        * secondary prolog
        * secondary template

        :param template: main template of code.
        :param secondary_template: template of code that will be inserted after the main one and rendered with it.
        :param kwargs: initial data.
        """

        self.__main_epilog = ""  # Code that will be inserted after the main template
        self.__secondary_prolog = (
            ""  # Code that will be inserted before the secondary template
        )
        self.__template = template
        self.__data = (
            kwargs  # Data to be inserted both into the main and secondary templates
        )
        self.__secondary_template = secondary_template
        self.__final = False

    def make_final(self) -> None:
        """
        Makes the code "final". Being "final" means that there will be no newline after the main part and will be additional newline after the secondary part. Thus, the code will consist of

        * main template
        * main epilog
        * secondary prolog
        * secondary template
        * \\\\n
        """

        self.__final = True

    def update_data(self, **kwargs) -> None:
        """
        Update data that will be used for rendering.

        :param kwargs: data to update.
        """

        self.__data.update(kwargs)

    def add_main_epilog(self, text: str):
        """
        Adds text to the end of the main epilog.

        :param text: text to add.
        """

        self.__main_epilog += text

    def add_secondary_prolog(self, text: str):
        # TODO: переименовать в secondary

        """
        Inserts text to the beginning of the secondary prolog.

        :param text: text to add.
        """

        self.__secondary_prolog = f"{text}{self.__secondary_prolog}"

    def render_main(self) -> str:
        """
        Renders and returns main part.
        """

        rendered = f"{self.__template.render(self.__data)}\n{self.__main_epilog}"

        if self.__final:
            return rendered[:-1]  # remove trailing \n

        return rendered

    def render_secondary(self) -> str:
        """
        Renders and returns secondary part.
        """

        rendered = self.__secondary_prolog

        if self.__secondary_template:
            rendered += f"\n{self.__secondary_template.render(self.__data)}"

        if self.__final:
            return f"{rendered}\n"

        return rendered

    def render(self) -> str:
        """
        Renders and returns the whole code (main + secondary).
        """

        return f"{self.render_main()}{self.render_secondary()}"

    def clear_secondary(self) -> None:
        self.__secondary_prolog = ""
        self.__secondary_template = None

    def __repr__(self) -> str:
        # TODO: remove
        return f"({repr(self.__template)}, {repr(self.__data)})"
