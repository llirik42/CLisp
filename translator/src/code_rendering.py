import os
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader, Template


__all__ = ["Code", "CodeCreator"]


class Code:
    def __init__(
        self, template: Template, secondary_template: Optional[Template] = None
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
        """

        self.__main_epilog = ""  # Code that will be inserted after the main template
        self.__secondary_prolog = (
            ""  # Code that will be inserted before the secondary template
        )
        self.__template = template
        self.__data = (
            {}
        )  # Data to be inserted both into the main and secondary templates
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


class CodeCreator:
    def __init__(self, templates_folder_path: str):
        """
        Class represents a creator for objects of Code.

        :param templates_folder_path: path to the directory with templates for code.
        :raises FileNotFoundError: the directory not found.
        """

        self.__env = Environment(loader=FileSystemLoader(templates_folder_path))
        self.__templates = {
            Path(name).stem: self.__env.get_template(name)
            for name in os.listdir(templates_folder_path)
        }

    def make_int(self) -> Code:
        """
        Returns code that creates an integer variable.

        :raises KeyError: template-file of the code not found.
        """

        return Code(
            template=self.__get_template("make_integer"),
            secondary_template=self.__get_template("destroy"),
        )

    def make_float(self) -> Code:
        """
        Returns code that creates a float variable.

        :raises KeyError: template-file of the code not found.
        """

        return Code(
            template=self.__get_template("make_float"),
            secondary_template=self.__get_template("destroy"),
        )

    def make_character(self) -> Code:
        """
        Returns code that creates a character variable.

        :raises KeyError: template-file of the code not found.
        """

        return Code(
            template=self.__get_template("make_character"),
            secondary_template=self.__get_template("destroy"),
        )

    def make_string(self) -> Code:
        """
        Returns code that creates a string variable.

        :raises KeyError: template-file of the code not found.
        """

        return Code(
            template=self.__get_template("make_string"),
            secondary_template=self.__get_template("destroy"),
        )

    def make_boolean(self) -> Code:
        """
        Returns code that creates a boolean variable.

        :raises KeyError: template-file of the code not found.
        """

        return Code(
            template=self.__get_template("make_boolean"),
            secondary_template=self.__get_template("destroy"),
        )

    def make_evaluable(self) -> Code:
        """
        Returns code that creates an evaluable variable.

        :raises KeyError: template-file of the code not found.
        """

        return Code(
            template=self.__get_template("make_evaluable"),
            secondary_template=self.__get_template("destroy"),
        )

    def function_call(self) -> Code:
        """
        Returns code that calls a function.

        :raises KeyError: template-file of the code not found.
        """

        return Code(
            template=self.__get_template("function_call"),
            secondary_template=self.__get_template("destroy"),
        )

    def condition(self) -> Code:
        """
        Returns code of condition (if).

        :raises KeyError: template-file of the code not found.
        """

        return Code(
            template=self.__get_template("condition"),
            secondary_template=self.__get_template("destroy"),
        )

    def main_function(self) -> Code:
        """
        Returns code that creates function main().

        :raises KeyError: template-file of the code not found.
        """

        return Code(
            template=self.__get_template("main_function"),
        )

    def __get_template(self, name: str) -> Template:
        """
        Returns template by the given name.

        :raises KeyError: template-file not found by the name.
        """

        return self.__templates[name]
