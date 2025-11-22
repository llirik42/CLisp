import os
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template

from src.code_rendering.codes import (
    EmptyCode,
    MakePrimitiveCode,
    MakeEvaluableCode,
    MakeLambdaCode,
    MakeListCode,
    MakeEnvironmentCode,
    GetVariableValueCode,
    SetVariableValueCode,
    UpdateVariableValueCode,
    LambdaCallCode,
    ProcedureCallCode,
    GetFunctionArgumentCode,
    LambdaDefinition,
    ProgramCode,
)
from src.symbols import Symbols


def check_required(data: dict[str, Any], required: list[str]) -> None:
    for r in required:
        if r not in data:
            raise KeyError(f'"{r}" is required')


def check_var(data: dict[str, Any]) -> None:
    check_required(data, ["var"])


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

    def empty(self) -> EmptyCode:
        c = EmptyCode()
        c.make_final_final()
        return c

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

    def get_func_arg(self) -> GetFunctionArgumentCode:
        def main_validate(data: dict) -> None:
            check_required(data, ["var", "array", "index"])

        return GetFunctionArgumentCode(
            main_template=self.__get_array_element_template(),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("object"),
            },
        )

    def procedure_call(self) -> ProcedureCallCode:
        def main_validate(data: dict) -> None:
            check_required(data, ["var", "func"])

        object_type = self.__symbols.find_internal_type("object")

        return ProcedureCallCode(
            main_template=self.__function_call_arg_list_template(),
            secondary_template=self.__function_call_template(),
            main_validate=main_validate,
            main_data={
                "type": object_type,
                "args_type": object_type,
            },
            secondary_data={"func": self.__symbols.find_internal_function("~object")},
        )

    def lambda_call(self) -> LambdaCallCode:
        def main_validate(data: dict) -> None:
            check_var(data)

            call_args = data["call_args"]
            if call_args[0] == "":
                raise KeyError(f'"lambda" is required')

        object_type = self.__symbols.find_internal_type("object")

        return LambdaCallCode(
            main_template=self.__function_call_arg_list_template(),
            secondary_template=self.__function_call_template(),
            main_validate=main_validate,
            main_data={
                "type": object_type,
                "args_type": object_type,
                "func": self.__symbols.find_internal_function("lambda_call"),
            },
            secondary_data={"func": self.__symbols.find_internal_function("~object")},
        )

    def lambda_definition(self) -> LambdaDefinition:
        def validate(data: dict) -> None:
            check_required(data, ["body", "ret"])

        return LambdaDefinition(
            main_template=self.__get_template("function_definition"),
            main_data={
                "ret_type": self.__symbols.find_internal_type("object"),
                "params": self.__symbols.find_internal_type("lambda_function_params"),
            },
            main_validate=validate,
        )

    def program(self, **kwargs) -> ProgramCode:
        def validate(data: dict) -> None:
            required = ["code"]

            for r in required:
                if r not in data:
                    raise KeyError(f'"{r}" is required')

        return ProgramCode(
            main_template=self.__get_template("program"), validate=validate, **kwargs
        )

    def __make_primitive(self, creation_function: str) -> MakePrimitiveCode:
        def main_validate(data: dict) -> None:
            check_var(data)

            if "args" not in data:
                raise KeyError(f'"value" is is required')

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
