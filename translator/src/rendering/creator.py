import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template

from .codes import (
    EmptyCode,
    MakePrimitiveCode,
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
    ConditionCode, MakeUnspecifiedCode,
)
from src.symbols import Symbols


class CodeCreator:
    def __init__(self, symbols: Symbols, templates_folder_path: str):
        """
        Class represents a creator for objects of Code.

        :param symbols: symbols that are used for code generating.
        :param templates_folder_path: path to the directory with templates for code.
        :raises FileNotFoundError: the directory not found.
        """

        self.__OBJECT_TYPE = symbols.find_internal_type("object")
        self.__ENVIRONMENT_TYPE = symbols.find_internal_type("environment")
        self.__DESTROY_OBJECT = symbols.find_internal_function("~object")
        self.__CREATE_UNSPECIFIED = symbols.find_internal_function("unspecified")
        self.__CREATE_INTEGER = symbols.find_internal_function("integer")
        self.__CREATE_FLOAT = symbols.find_internal_function("float")
        self.__CREATE_STRING = symbols.find_internal_function("string")
        self.__CREATE_CHARACTER = symbols.find_internal_function("character")
        self.__CREATE_BOOLEAN = symbols.find_internal_function("boolean")
        self.__CREATE_LAMBDA = symbols.find_internal_function("lambda")
        self.__CREATE_LIST = symbols.find_internal_function("list")
        self.__OBJECT_TO_BOOLEAN = symbols.find_internal_function("to_boolean")
        self.__CREATE_ENVIRONMENT = symbols.find_internal_function("environment")
        self.__DESTROY_ENVIRONMENT = symbols.find_internal_function("~environment")
        self.__GET_GLOBAL_ENVIRONMENT = symbols.find_internal_function(
            "environment_global"
        )
        self.__GET_VARIABLE_VALUE = symbols.find_internal_function("get_variable_value")
        self.__SET_VARIABLE_VALUE = symbols.find_internal_function("set_variable_value")
        self.__UPDATE_VARIABLE_VALUE = symbols.find_internal_function(
            "update_variable_value"
        )
        self.__CALL_LAMBDA = symbols.find_internal_function("lambda_call")
        self.__FUNCTION_ARGS_VAR = "args"
        self.__FUNCTION_PARAMS = symbols.find_internal_type("lambda_function_params")

        self.__load_templates(templates_folder_path)

    def empty(self) -> EmptyCode:
        return EmptyCode()

    def make_unspecified(self) -> MakeUnspecifiedCode:
        return MakeUnspecifiedCode(
            main_template=self.__get_template("make_primitive"),
            secondary_template=self.__get_destroy_object_template(),
            main_data={
                "type": self.__OBJECT_TYPE,
                "func": self.__CREATE_UNSPECIFIED,
            },
            secondary_data={
                "func": self.__DESTROY_OBJECT,
            },
        )

    def make_int(self) -> MakePrimitiveCode:
        return self.__make_primitive(self.__CREATE_INTEGER)

    def make_float(self) -> MakePrimitiveCode:
        return self.__make_primitive(self.__CREATE_FLOAT)

    def make_string(self) -> MakePrimitiveCode:
        return self.__make_primitive(self.__CREATE_STRING)

    def make_character(self) -> MakePrimitiveCode:
        return self.__make_primitive(self.__CREATE_CHARACTER)

    def make_boolean(self) -> MakePrimitiveCode:
        return self.__make_primitive(self.__CREATE_BOOLEAN)

    def make_lambda(self) -> MakeLambdaCode:
        return MakeLambdaCode(
            main_template=self.__get_template("make_lambda"),
            secondary_template=self.__get_destroy_object_template(),
            main_data={
                "type": self.__OBJECT_TYPE,
                "creation_func": self.__CREATE_LAMBDA,
            },
            secondary_data={"func": self.__DESTROY_OBJECT},
        )

    def make_list(self) -> MakeListCode:
        return MakeListCode(
            main_template=self.__get_template("make_list"),
            secondary_template=self.__get_destroy_object_template(),
            main_data={
                "type": self.__OBJECT_TYPE,
                "func": self.__CREATE_LIST,
            },
            secondary_data={
                "func": self.__DESTROY_OBJECT,
            },
        )

    def condition(self) -> ConditionCode:
        return ConditionCode(
            main_template=self.__get_template("condition"),
            secondary_template=self.__get_destroy_object_template(),
            main_data={"type": self.__OBJECT_TYPE, "func": self.__OBJECT_TO_BOOLEAN},
            secondary_data={"func": self.__DESTROY_OBJECT},
        )

    def make_environment(self) -> MakeEnvironmentCode:
        return MakeEnvironmentCode(
            main_template=self.__get_template("make_environment"),
            secondary_template=self.__get_template("destroy_environment"),
            main_data={
                "type": self.__ENVIRONMENT_TYPE,
                "func": self.__CREATE_ENVIRONMENT,
            },
            secondary_data={"func": self.__DESTROY_ENVIRONMENT},
        )

    def get_global_environment(self) -> GetGlobalEnvironmentCode:
        return GetGlobalEnvironmentCode(
            main_template=self.__get_template("get_global_environment"),
            secondary_template=self.__get_template("destroy_environment"),
            main_data={
                "type": self.__ENVIRONMENT_TYPE,
                "func": self.__GET_GLOBAL_ENVIRONMENT,
            },
            secondary_data={"func": self.__DESTROY_ENVIRONMENT},
        )

    def get_variable_value(self) -> GetVariableValueCode:
        return GetVariableValueCode(
            main_template=self.__get_template("get_variable_value"),
            main_data={
                "type": self.__OBJECT_TYPE,
                "func": self.__GET_VARIABLE_VALUE,
            },
        )

    def set_variable_value(self) -> SetVariableValueCode:
        return SetVariableValueCode(
            main_template=self.__get_template("set_variable_value"),
            main_data={
                "type": self.__OBJECT_TYPE,
                "func": self.__SET_VARIABLE_VALUE,
            },
        )

    def update_variable_value(self) -> UpdateVariableValueCode:
        return UpdateVariableValueCode(
            main_template=self.__get_template("update_variable_value"),
            secondary_template=self.__get_destroy_object_template(),
            main_data={
                "type": self.__OBJECT_TYPE,
                "func": self.__UPDATE_VARIABLE_VALUE,
            },
            secondary_data={
                "func": self.__DESTROY_OBJECT,
            },
        )

    def get_function_argument(self) -> GetFunctionArgumentCode:
        return GetFunctionArgumentCode(
            main_template=self.__get_template("get_function_argument"),
            main_data={
                "type": self.__OBJECT_TYPE,
                "args": self.__FUNCTION_ARGS_VAR,
            },
        )

    def procedure_call(self) -> ProcedureCallCode:
        return ProcedureCallCode(
            main_template=self.__get_template("procedure_call"),
            secondary_template=self.__get_destroy_object_template(),
            main_data={"type": self.__OBJECT_TYPE},
            secondary_data={"func": self.__DESTROY_OBJECT},
        )

    def lambda_call(self) -> LambdaCallCode:
        return LambdaCallCode(
            main_template=self.__get_template("lambda_call"),
            secondary_template=self.__get_destroy_object_template(),
            main_data={
                "type": self.__OBJECT_TYPE,
                "args_type": self.__OBJECT_TYPE,
                "func": self.__CALL_LAMBDA,
            },
            secondary_data={
                "func": self.__DESTROY_OBJECT,
            },
        )

    def lambda_definition(self) -> LambdaDefinitionCode:
        return LambdaDefinitionCode(
            main_template=self.__get_template("lambda_definition"),
            main_data={
                "ret_type": self.__OBJECT_TYPE,
                "params": self.__FUNCTION_PARAMS,
            },
        )

    def program(self) -> ProgramCode:
        return ProgramCode(
            main_template=self.__get_template("program"),
        )

    def __make_primitive(self, creation_function: str) -> MakePrimitiveCode:
        return MakePrimitiveCode(
            main_template=self.__get_template("make_primitive"),
            secondary_template=self.__get_destroy_object_template(),
            main_data={
                "type": self.__OBJECT_TYPE,
                "func": creation_function,
            },
            secondary_data={
                "func": self.__DESTROY_OBJECT,
            },
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

        env = Environment(loader=FileSystemLoader(templates_folder_path))

        self.__templates = {
            Path(name).stem: env.get_template(name)
            for name in os.listdir(templates_folder_path)
        }
