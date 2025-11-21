import os
from pathlib import Path

from src.standard_elements import StandardElements

from jinja2 import Environment, FileSystemLoader, Template

from .code import Code


class CodeCreator:
    def __init__(self, standard_elements: StandardElements, templates_folder_path: str):
        """
        Class represents a creator for objects of Code.

        :param templates_folder_path: path to the directory with templates for code.
        :raises FileNotFoundError: the directory not found.
        """

        self.__standard_elements = standard_elements
        self.__env = Environment(loader=FileSystemLoader(templates_folder_path))
        self.__load_templates(templates_folder_path)

    def make_float(self, **kwargs) -> Code:
        return self.make_constant(function=self.__standard_elements.get_internal("float"), **kwargs)

    def make_int(self, **kwargs) -> Code:
        return self.make_constant(function=self.__standard_elements.get_internal("integer"), **kwargs)

    def make_string(self, **kwargs) -> Code:
        return self.make_constant(function=self.__standard_elements.get_internal("string"), **kwargs)

    def make_character(self, **kwargs) -> Code:
        return self.make_constant(function=self.__standard_elements.get_internal("character"), **kwargs)

    def make_boolean(self, **kwargs) -> Code:
        return self.make_constant(function=self.__standard_elements.get_internal("boolean"), **kwargs)

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

    def make_lambda(self, **kwargs) -> Code:
        """
        Returns code that creates an lambda variable.

        :param kwargs: initial data in the code.
        :raises KeyError: template-file of the code not found.
        """

        return Code(
            template=self.__get_template("make_lambda"),
            secondary_template=self.__get_template("destroy_object"),
            **kwargs,
        )

    def declare_function(self, **kwargs) -> Code:
        """
        Returns code that declares a function.

        :param kwargs: initial data in the code.
        :raises KeyError: template-file of the code not found.
        """

        return Code(
            template=self.__get_template("declare_function"),
            **kwargs,
        )

    def get_arg(self, **kwargs) -> Code:
        """
        Returns code that gets an arg of the function.

        :param kwargs: initial data in the code.
        :raises KeyError: template-file of the code not found.
        """

        return Code(
            template=self.__get_template("get_arg"),
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
