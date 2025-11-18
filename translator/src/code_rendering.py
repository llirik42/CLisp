import os
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader, Template


__all__ = ["Code", "wrap_codes", "CodeCreator"]


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


# TODO: сделать лишь один параметр - список кодов (изменить документацию)
def wrap_codes(codes: list[Code]) -> Code:
    """
    Function wraps start code into the wrapping ones.

    **Example**

    start code::

        func11()  # main part

        func12()  # secondary part

    wrapping code[0]::

        func21()  # main part

        func22()  # secondary part

    wrapping code[1]::

        func31()  # main part

        func32()  # secondary part

    result::

        # main part
        func11()
        func21()
        func31()

        # secondary part
        func32()
        func22()
        func12()
    """

    code = codes[0]

    for c in codes[:0:-1]:
        c.add_main_epilog(code.render_main())
        c.add_secondary_prolog(code.render_secondary())
        code = c

    return code


def nest_codes(codes: list[Code]) -> Code:
    # TODO: add pydoc

    reversed_codes = codes[::-1]

    code = reversed_codes[0]
    for c in reversed_codes[1:]:
        c.add_main_epilog(code.render_main())
        c.add_secondary_prolog(code.render_secondary())
        code = c

    return code


def join_codes(codes: list[Code]) -> str:
    rendered = [c.render() for c in codes]
    return "\n".join(rendered)

class CodeCreator:
    def __init__(self, templates_folder_path: str):
        """
        Class represents a creator for objects of Code.

        :param templates_folder_path: path to the directory with templates for code.
        :raises FileNotFoundError: the directory not found.
        """

        self.__env = Environment(loader=FileSystemLoader(templates_folder_path))
        self.__load_templates(templates_folder_path)

    def make_constant(self, **kwargs) -> Code:
        """
        Returns code that creates a constant.

        :param kwargs: initial data in the code.
        :raises KeyError: template-file of the code not found.
        """

        return Code(
            template=self.__get_template("make_constant"),
            secondary_template=self.__get_template("destroy_object"),
            **kwargs,
        )

    def make_evaluable(self, **kwargs) -> Code:
        """
        Returns code that creates an evaluable variable.

        :param kwargs: initial data in the code.
        :raises KeyError: template-file of the code not found.
        """

        return Code(
            template=self.__get_template("make_evaluable"),
            secondary_template=self.__get_template("destroy_object"),
            **kwargs,
        )

    def function_call(self, **kwargs) -> Code:
        """
        Returns code that calls a function.

        :param kwargs: initial data in the code.
        :raises KeyError: template-file of the code not found.
        """

        return Code(
            template=self.__get_template("function_call"),
            secondary_template=self.__get_template("destroy_object"),
            **kwargs,
        )

    def main_function(self, **kwargs) -> Code:
        """
        Returns code that creates function main().

        :param kwargs: initial data in the code.
        :raises KeyError: template-file of the code not found.
        """

        return Code(template=self.__get_template("main_function"), **kwargs)

    def get_variable_value(self, **kwargs) -> Code:
        """
        Returns code that obtains value of the variable.

        :param kwargs: initial data in the code.
        :raises KeyError: template-file of the code not found.
        """

        return Code(template=self.__get_template("get_variable_value"), **kwargs)

    def set_variable_value(self, **kwargs) -> Code:
        """
        Returns code that defines a variable with the value.

        :param kwargs: initial data in the code.
        :raises KeyError: template-file of the code not found.
        """

        return Code(template=self.__get_template("set_variable_value"), **kwargs)

    def update_variable_value(self, **kwargs) -> Code:
        """
        Returns code that changes value of the variable.

        :param kwargs: initial data in the code.
        :raises KeyError: template-file of the code not found.
        """

        return Code(
            template=self.__get_template("update_variable_value"),
            secondary_template=self.__get_template("destroy_object"),
            **kwargs,
        )

    def make_environment(self, **kwargs) -> Code:
        """
        Returns code that creates an environment.

        :param kwargs: initial data in the code.
        :raises KeyError: template-file of the code not found.
        """

        return Code(
            template=self.__get_template("make_environment"),
            secondary_template=self.__get_template("destroy_environment"),
            **kwargs,
        )

    def __get_template(self, name: str) -> Template:
        """
        Returns template by the given name.

        :raises KeyError: template-file not found by the name.
        """

        return self.__templates[name]

    def __load_templates(self, templates_folder_path: str) -> None:
        """
        Loads all templates from the given folder.

        :param templates_folder_path: path to the directory with templates for code.
        :raises FileNotFoundError: the directory not found.
        """

        self.__templates = {
            Path(name).stem: self.__env.get_template(name)
            for name in os.listdir(templates_folder_path)
        }
