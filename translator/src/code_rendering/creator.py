import os
from pathlib import Path
from typing import Any

from src.code_rendering.codes.get_variable_value import GetVariableValueCode
from src.code_rendering.codes.make_environment import MakeEnvironmentCode
from src.code_rendering.codes.make_evaluable import MakeEvaluableCode
from src.code_rendering.codes.make_lambda import MakeLambdaCode
from src.code_rendering.codes.make_list import MakeListCode
from src.code_rendering.codes.make_primitive import MakePrimitiveCode
from src.code_rendering.codes.set_variable_code import SetVariableValueCode
from src.code_rendering.codes.update_variable_code import UpdateVariableValueCode
from src.symbols import Symbols

from jinja2 import Environment, FileSystemLoader, Template

from src.code_rendering.codes.code import Code


def check_var(data: dict[str, Any]) -> None:
    if "var" not in data:
        raise KeyError(f'"var" is required')


class CodeCreator:
    def __init__(self, symbols: Symbols, templates_folder_path: str):
        """
        Class represents a creator for objects of Code.

        :param templates_folder_path: path to the directory with templates for code.
        :raises FileNotFoundError: the directory not found.
        """

        self.__symbols = symbols
        self.__env = Environment(loader=FileSystemLoader(templates_folder_path))
        self.__load_templates(templates_folder_path)

    def make_int(self) -> MakePrimitiveCode:
        return self.__make_primitive(self.__symbols.find_internal_function("integer"))

    def make_float(self) -> MakePrimitiveCode:
        return self.__make_primitive(self.__symbols.find_internal_function("float"))

    def make_string(self) -> MakePrimitiveCode:
        return self.__make_primitive(self.__symbols.find_internal_function("string"))

    def make_character(self) -> MakePrimitiveCode:
        return self.__make_primitive(self.__symbols.find_internal_function("character"))

    def make_boolean(self) -> MakePrimitiveCode:
        return self.__make_primitive(self.__symbols.find_internal_function("boolean"))

    def make_evaluable(self) -> MakeEvaluableCode:
        def main_validate(data: dict) -> None:
            check_var(data)

            call_args = data["call_args"]
            if call_args[0] == "":
                raise KeyError(f'"func" is required')

        object_type = self.__symbols.find_internal_type("object")

        return MakeEvaluableCode(
            main_template=self.__function_call_arg_list_template(),
            secondary_template=self.__function_call_template(),
            main_validate=main_validate,
            main_data={
                "type": object_type,
                "args_type": object_type,
                "func": self.__symbols.find_internal_function("evaluable"),
            },
            secondary_data={"func": self.__symbols.find_internal_function("~object")},
        )

    def make_lambda(self) -> MakeLambdaCode:
        def main_validate(data: dict) -> None:
            check_var(data)

            args = data["args"]
            if args[0] == "":
                raise KeyError(f'"func" is required')

        return MakeLambdaCode(
            main_template=self.__function_call_template(),
            secondary_template=self.__function_call_template(),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("object"),
                "func": self.__symbols.find_internal_function("lambda"),
            },
            secondary_data={"func": self.__symbols.find_internal_function("~object")},
        )

    def make_list(self) -> MakeListCode:
        def main_validate(data: dict) -> None:
            check_var(data)

            args = data["args"]
            if args[0] == "":
                raise KeyError(f'"element_count" is required')
            if args[1] == "":
                raise KeyError(f'"element_pointer" is required')

        return MakeListCode(
            main_template=self.__function_call_template(),
            secondary_template=self.__function_call_template(),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("object"),
                "func": self.__symbols.find_internal_function("list"),
            },
            secondary_data={"func": self.__symbols.find_internal_function("~object")},
        )

    def make_environment(self) -> MakeEnvironmentCode:
        def main_validate(data: dict) -> None:
            check_var(data)

        return MakeEnvironmentCode(
            main_template=self.__function_call_template(),
            secondary_template=self.__function_call_template(),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("object"),
                "func": self.__symbols.find_internal_function("environment"),
            },
            secondary_data={
                "func": self.__symbols.find_internal_function("~environment")
            },
        )

    def get_variable_value(self) -> GetVariableValueCode:
        def main_validate(data: dict) -> None:
            check_var(data)

            args = data["args"]
            if args[0] == "":
                raise KeyError(f'"env" is required')
            if args[1] == "":
                raise KeyError(f'"name" is required')

        return GetVariableValueCode(
            main_template=self.__function_call_template(),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("object"),
                "func": self.__symbols.find_internal_function("get_variable_value"),
            },
        )

    def set_variable_value(self) -> SetVariableValueCode:
        def main_validate(data: dict) -> None:
            args = data["args"]
            if args[0] == "":
                raise KeyError(f'"env" is required')
            if args[1] == "":
                raise KeyError(f'"name" is required')
            if args[2] == "":
                raise KeyError(f'"value" is required')

        return SetVariableValueCode(
            main_template=self.__function_call_template(),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("object"),
                "func": self.__symbols.find_internal_function("set_variable_value"),
            },
        )

    def update_variable_value(self) -> UpdateVariableValueCode:
        def main_validate(data: dict) -> None:
            check_var(data)

            args = data["args"]
            if args[0] == "":
                raise KeyError(f'"env" is required')
            if args[1] == "":
                raise KeyError(f'"name" is required')
            if args[2] == "":
                raise KeyError(f'"value" is required')

        return UpdateVariableValueCode(
            main_template=self.__function_call_template(),
            main_validate=main_validate,
            secondary_template=self.__function_call_template(),
            main_data={
                "type": self.__symbols.find_internal_type("object"),
                "func": self.__symbols.find_internal_function("set_variable_value"),
            },
            secondary_data={"func": self.__symbols.find_internal_function("~object")},
        )

    def declare_function(self, **kwargs) -> Code:
        """
        Returns code that declares a function.

        :param kwargs: initial data in the code.
        :raises KeyError: template-file of the code not found.
        """

        def validate(data: dict) -> None:
            required = ["code", "ret_type", "func"]

            for r in required:
                if r not in data:
                    raise KeyError(f'"{r}" is required')

        return Code(
            main_template=self.__get_template("declare_function"),
            validate=validate,
            **kwargs,
        )

    def get_arg(self, **kwargs) -> Code:
        """
        Returns code that gets an arg of the function.

        :param kwargs: initial data in the code.
        :raises KeyError: template-file of the code not found.
        """

        return Code(
            main_template=self.__get_template("get_arg"),
            **kwargs,
        )

    def function_call(self, **kwargs) -> Code:
        def validate(data: dict) -> None:
            if "func" not in data:
                raise KeyError('"func" is required')

            if "var" in data and "type" not in data:
                raise KeyError('"type" is required while "var" is present')

        return Code(
            main_template=self.__get_template("function_call"),
            validate=validate,
            **kwargs,
        )

    def function_call_arg_list(self, **kwargs) -> Code:
        def validate(data: dict) -> None:
            required = ["args_var", "func", "args_type"]

            for r in required:
                if r not in data:
                    raise KeyError(f'"{r}" is required')

            if "var" in data and "type" not in data:
                raise KeyError('"type" is required while "var" is present')

        return Code(
            main_template=self.__get_template("function_call_arg_list"),
            validate=validate,
            **kwargs,
        )

    def get_array_element(self, **kwargs) -> Code:
        def validate(data: dict) -> None:
            required = ["type", "var", "array", "index"]

            for r in required:
                if r not in data:
                    raise KeyError(f'"{r}" is required')

        return Code(
            main_template=self.__get_template("get_array_element"),
            validate=validate,
            **kwargs,
        )

    def function_call_old(self, **kwargs) -> Code:
        """
        Returns code that calls a function.

        :param kwargs: initial data in the code.
        :raises KeyError: template-file of the code not found.
        """

        return Code(
            main_template=self.__get_template("function_call"),
            secondary_template=self.__get_template("destroy_object"),
            **kwargs,
        )

    def program(self, **kwargs) -> Code:
        """
        Returns code that creates function main().

        :param kwargs: initial data in the code.
        :raises KeyError: template-file of the code not found.
        """

        def validate(data: dict) -> None:
            required = ["code"]

            for r in required:
                if r not in data:
                    raise KeyError(f'"{r}" is required')

        return Code(
            main_template=self.__get_template("program"), validate=validate, **kwargs
        )

    def __make_primitive(self, creation_function: str) -> MakePrimitiveCode:
        def main_validate(data: dict) -> None:
            check_var(data)

            if "args" not in data:
                raise KeyError(f'"value" is is required')  # See MakePrimitiveCode

        return MakePrimitiveCode(
            main_template=self.__function_call_template(),
            secondary_template=self.__function_call_template(),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("object"),
                "func": creation_function,
            },
            secondary_data={"func": self.__symbols.find_internal_function("~object")},
        )

    def __declare_function__template(self) -> Template:
        return self.__get_template("declare_function")

    def __function_call_template(self) -> Template:
        return self.__get_template("function_call")

    def __function_call_arg_list_template(self) -> Template:
        return self.__get_template("function_call_arg_list")

    def __get_array_element_template(self) -> Template:
        return self.__get_template("get_array_element")

    def __program_template(self) -> Template:
        return self.__get_template("program")

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
