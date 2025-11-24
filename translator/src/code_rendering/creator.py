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
    LambdaDefinitionCode,
    ProgramCode,
    GetGlobalEnvironmentCode,
    DestroyGlobalEnvironmentCode,
    DestroyObjectCode,
)
from src.code_rendering.codes.global_environment_creation import (
    GlobalEnvironmentCreation,
)
from src.code_rendering.codes.global_environment_destroying import (
    GlobalEnvironmentDestroying,
)
from src.symbols import Symbols


def check_required(data: dict[str, Any], *args) -> None:
    for r in args:
        if r not in data:
            raise KeyError(f'"{r}" is required')


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
        c = EmptyCode(empty=True)
        c.make_final_final()

        return c

    def destroy_object(self) -> DestroyObjectCode:
        def main_validate(data: dict) -> None:
            check_required(data, "var")

        return DestroyObjectCode(
            main_template=self.__get_template("destroy_object"),
            main_validate=main_validate,
            main_data={
                "func": self.__symbols.find_internal_function("~object"),
            },
        )

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
            check_required(data, "var", "func")

        return MakeEvaluableCode(
            main_template=self.__get_template("make_evaluable"),
            secondary_template=self.__get_destroy_object_template(),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("object"),
                "creation_func": self.__symbols.find_internal_function("evaluable"),
            },
            secondary_data={"func": self.__symbols.find_internal_function("~object")},
        )

    def make_lambda(self) -> MakeLambdaCode:
        def main_validate(data: dict) -> None:
            check_required(data, "var", "func")

        return MakeLambdaCode(
            main_template=self.__get_template("make_lambda"),
            secondary_template=self.__get_destroy_object_template(),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("object"),
                "creation_func": self.__symbols.find_internal_function("lambda"),
            },
            secondary_data={"func": self.__symbols.find_internal_function("~object")},
        )

    def make_list(self) -> MakeListCode:
        def main_validate(data: dict) -> None:
            check_required(data, "var")

        return MakeListCode(
            main_template=self.__get_template("make_list"),
            secondary_template=self.__get_destroy_object_template(),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("object"),
                "func": self.__symbols.find_internal_function("list"),
            },
            secondary_data={"func": self.__symbols.find_internal_function("~object")},
        )

    def make_environment(self) -> MakeEnvironmentCode:
        def main_validate(data: dict) -> None:
            check_required(data, "var")

        return MakeEnvironmentCode(
            main_template=self.__get_template("make_environment"),
            secondary_template=self.__get_template("destroy_environment"),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("environment"),
                "func": self.__symbols.find_internal_function("environment"),
            },
            secondary_data={
                "func": self.__symbols.find_internal_function("~environment")
            },
        )

    def get_global_environment(self) -> GetGlobalEnvironmentCode:
        def main_validate(data: dict) -> None:
            check_required(data, "var")

            if "func" not in data:
                raise KeyError(f'"get_func" is required')

        return GetGlobalEnvironmentCode(
            main_template=self.__get_template("get_global_environment"),
            secondary_template=self.__get_template("destroy_environment"),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("environment"),
            },
            secondary_data={
                "func": self.__symbols.find_internal_function("~environment")
            }
        )

    def destroy_global_environment(self) -> DestroyGlobalEnvironmentCode:
        def main_validate(data: dict) -> None:
            check_required(data, "var")

        return DestroyGlobalEnvironmentCode(
            main_template=self.__get_template("make_environment"),
            secondary_template=self.__get_template("destroy_environment"),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("environment"),
                "func": self.__symbols.find_internal_function("environment"),
            },
            secondary_data={
                "func": self.__symbols.find_internal_function("~environment")
            },
        )

    def get_variable_value(self) -> GetVariableValueCode:
        def main_validate(data: dict) -> None:
            check_required(data, "var", "env", "name")

        return GetVariableValueCode(
            main_template=self.__get_template("get_variable_value"),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("object"),
                "func": self.__symbols.find_internal_function("get_variable_value"),
            },
        )

    def set_variable_value(self) -> SetVariableValueCode:
        def main_validate(data: dict) -> None:
            check_required(data, "env", "name", "value")

        return SetVariableValueCode(
            main_template=self.__get_template("set_variable_value"),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("object"),
                "func": self.__symbols.find_internal_function("set_variable_value"),
            },
        )

    def update_variable_value(self) -> UpdateVariableValueCode:
        def main_validate(data: dict) -> None:
            check_required(data, "var", "env", "name", "value")

        return UpdateVariableValueCode(
            main_template=self.__get_template("update_variable_value"),
            main_validate=main_validate,
            secondary_template=self.__get_destroy_object_template(),
            main_data={
                "type": self.__symbols.find_internal_type("object"),
                "func": self.__symbols.find_internal_function("update_variable_value"),
            },
            secondary_data={"func": self.__symbols.find_internal_function("~object")},
        )

    def get_function_argument(self) -> GetFunctionArgumentCode:
        def main_validate(data: dict) -> None:
            check_required(data, "var", "index")

        args = "args"

        return GetFunctionArgumentCode(
            main_template=self.__get_template("get_function_argument"),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("object"),
                "args": args,
            },
        )

    def procedure_call(self) -> ProcedureCallCode:
        def main_validate(data: dict) -> None:
            check_required(data, "var", "func")

        return ProcedureCallCode(
            main_template=self.__get_template("procedure_call"),
            secondary_template=self.__get_destroy_object_template(),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("object"),
            },
            secondary_data={"func": self.__symbols.find_internal_function("~object")},
        )

    def lambda_call(self) -> LambdaCallCode:
        def main_validate(data: dict) -> None:
            check_required(data, "var", "lambda_var")

        object_type = self.__symbols.find_internal_type("object")

        return LambdaCallCode(
            main_template=self.__get_template("lambda_call"),
            secondary_template=self.__get_destroy_object_template(),
            main_validate=main_validate,
            main_data={
                "type": object_type,
                "args_type": object_type,
                "func": self.__symbols.find_internal_function("lambda_call"),
            },
            secondary_data={"func": self.__symbols.find_internal_function("~object")},
        )

    def lambda_definition(self) -> LambdaDefinitionCode:
        def validate(data: dict) -> None:
            check_required(data, "body", "ret_var", "func")

        return LambdaDefinitionCode(
            main_template=self.__get_template("lambda_definition"),
            main_data={
                "ret_type": self.__symbols.find_internal_type("object"),
                "params": self.__symbols.find_internal_type("lambda_function_params"),
            },
            main_validate=validate,
        )

    def global_environment_creation(self) -> GlobalEnvironmentCreation:
        def validate(data: dict) -> None:
            check_required(data, "func", "var", "body")

        return GlobalEnvironmentCreation(
            main_template=self.__get_template("global_environment_creation"),
            main_data={
                "type": self.__symbols.find_internal_type("environment"),
            },
            main_validate=validate,
        )

    def global_environment_destroying(self) -> GlobalEnvironmentDestroying:
        def validate(data: dict) -> None:
            check_required(data, "func", "var", "body")

        return GlobalEnvironmentDestroying(
            main_template=self.__get_template("global_environment_destroying"),
            main_data={
                "type": self.__symbols.find_internal_type("environment"),
            },
            main_validate=validate,
        )

    def program(self) -> ProgramCode:
        def main_validate(data: dict) -> None:
            pass

        return ProgramCode(
            main_template=self.__get_template("program"),
            main_validate=main_validate,
        )

    def __make_primitive(self, creation_function: str) -> MakePrimitiveCode:
        def main_validate(data: dict) -> None:
            check_required(data, "var", "value")

        return MakePrimitiveCode(
            main_template=self.__get_template("make_primitive"),
            secondary_template=self.__get_destroy_object_template(),
            main_validate=main_validate,
            main_data={
                "type": self.__symbols.find_internal_type("object"),
                "func": creation_function,
            },
            secondary_data={"func": self.__symbols.find_internal_function("~object")},
        )

    def __get_destroy_object_template(self) -> Template:
        return self.__get_template("destroy_object")

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
