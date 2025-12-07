import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template

from .codes import (
    EmptyCode,
    MakePrimitiveCode,
    MakeListFromArrayCode,
    MakeEnvironmentCode,
    GetVariableValueCode,
    SetVariableValueCode,
    UpdateVariableValueCode,
    LambdaCallCode,
    FunctionDefinitionCode,
    ProgramCode,
    ConditionCode,
    HavingVarCode,
    MakeCallableCode,
    EvaluationCode,
    NativeCallCode,
    LoopCode,
    GetBooleanValueCode, MoveEnvironmentCode,
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

        self.__symbols = symbols

        self.__load_templates(templates_folder_path)

    def empty(self) -> EmptyCode:
        return EmptyCode()

    def make_unspecified(self) -> HavingVarCode:
        return HavingVarCode(
            main_template=self.__get_template("make_primitive"),
            secondary_template=self.__get_decrease_ref_count_template(),
            main_data={
                "type": self.__symbols.OBJECT_TYPE,
                "func": self.__symbols.CREATE_UNSPECIFIED,
            },
            secondary_data={
                "func": self.__symbols.DECREASE_REF_COUNT,
            },
        )

    def make_int(self) -> MakePrimitiveCode:
        return self.__make_primitive(self.__symbols.CREATE_INTEGER)

    def make_float(self) -> MakePrimitiveCode:
        return self.__make_primitive(self.__symbols.CREATE_FLOAT)

    def make_string(self) -> MakePrimitiveCode:
        return self.__make_primitive(self.__symbols.CREATE_STRING)

    def make_character(self) -> MakePrimitiveCode:
        return self.__make_primitive(self.__symbols.CREATE_CHARACTER)

    def make_true(self) -> HavingVarCode:
        return HavingVarCode(
            main_template=self.__get_template("make_primitive"),
            secondary_template=self.__get_decrease_ref_count_template(),
            main_data={
                "type": self.__symbols.OBJECT_TYPE,
                "func": self.__symbols.CREATE_TRUE,
            },
            secondary_data={
                "func": self.__symbols.DECREASE_REF_COUNT,
            },
        )

    def make_false(self) -> HavingVarCode:
        return HavingVarCode(
            main_template=self.__get_template("make_primitive"),
            secondary_template=self.__get_decrease_ref_count_template(),
            main_data={
                "type": self.__symbols.OBJECT_TYPE,
                "func": self.__symbols.CREATE_FALSE,
            },
            secondary_data={
                "func": self.__symbols.DECREASE_REF_COUNT,
            },
        )

    def make_lambda(self) -> MakeCallableCode:
        return self.__make_callable(self.__symbols.CREATE_LAMBDA)

    def make_evaluable(self) -> MakeCallableCode:
        return self.__make_callable(self.__symbols.CREATE_EVALUABLE)

    def make_list_from_array(self) -> MakeListFromArrayCode:
        return MakeListFromArrayCode(
            main_template=self.__get_template("make_list_from_array"),
            secondary_template=self.__get_decrease_ref_count_template(),
            main_data={
                "type": self.__symbols.OBJECT_TYPE,
                "func": self.__symbols.CREATE_LIST_FROM_ARRAY,
            },
            secondary_data={
                "func": self.__symbols.DECREASE_REF_COUNT,
            },
        )

    def if_(self) -> ConditionCode:
        return ConditionCode(
            main_template=self.__get_template("if"),
            secondary_template=self.__get_decrease_ref_count_template(),
            main_data={"type": self.__symbols.OBJECT_TYPE, "func": self.__symbols.OBJECT_TO_BOOLEAN},
            secondary_data={"func": self.__symbols.DECREASE_REF_COUNT},
        )

    def increase_ref_count(self) -> HavingVarCode:
        return HavingVarCode(
            main_template=self.__get_template("increase_ref_count"),
            main_data={"func": self.__symbols.INCREASE_REF_COUNT},
        )

    def decrease_ref_count(self) -> HavingVarCode:
        return HavingVarCode(
            main_template=self.__get_template("decrease_ref_count"),
            main_data={"func": self.__symbols.DECREASE_REF_COUNT},
        )

    def make_environment(self) -> MakeEnvironmentCode:
        return MakeEnvironmentCode(
            main_template=self.__get_template("make_environment"),
            secondary_template=self.__get_template("destroy_environment"),
            main_data={
                "type": self.__symbols.ENVIRONMENT_TYPE,
                "func": self.__symbols.CREATE_ENVIRONMENT,
            },
            secondary_data={"func": self.__symbols.DESTROY_ENVIRONMENT},
        )

    def get_global_environment(self) -> HavingVarCode:
        return HavingVarCode(
            main_template=self.__get_template("get_global_environment"),
            secondary_template=self.__get_template("destroy_environment"),
            main_data={
                "type": self.__symbols.ENVIRONMENT_TYPE,
                "func": self.__symbols.GET_GLOBAL_ENVIRONMENT,
            },
            secondary_data={"func": self.__symbols.DESTROY_GLOBAL_ENVIRONMENT},
        )

    def get_variable_value(self) -> GetVariableValueCode:
        return GetVariableValueCode(
            main_template=self.__get_template("get_variable_value"),
            main_data={
                "type": self.__symbols.OBJECT_TYPE,
                "func": self.__symbols.GET_VARIABLE_VALUE,
            },
        )

    def set_variable_value(self) -> SetVariableValueCode:
        return SetVariableValueCode(
            main_template=self.__get_template("set_variable_value"),
            main_data={
                "type": self.__symbols.OBJECT_TYPE,
                "func": self.__symbols.SET_VARIABLE_VALUE,
            },
        )

    def update_variable_value(self) -> UpdateVariableValueCode:
        return UpdateVariableValueCode(
            main_template=self.__get_template("update_variable_value"),
            secondary_template=self.__get_decrease_ref_count_template(),
            main_data={
                "type": self.__symbols.OBJECT_TYPE,
                "func": self.__symbols.UPDATE_VARIABLE_VALUE,
            },
            secondary_data={
                "func": self.__symbols.DECREASE_REF_COUNT,
            },
        )

    def lambda_call(self) -> LambdaCallCode:
        return self.__lambda_call(self.__symbols.CALL_LAMBDA)

    def lambda_call_list(self) -> LambdaCallCode:
        return self.__lambda_call(self.__symbols.CALL_LAMBDA_LIST)

    def evaluation(self) -> EvaluationCode:
        return EvaluationCode(
            main_template=self.__get_template("evaluation"),
            secondary_template=self.__get_decrease_ref_count_template(),
            main_data={
                "type": self.__symbols.OBJECT_TYPE,
                "func": self.__symbols.EVALUATE,
            },
            secondary_data={
                "func": self.__symbols.DECREASE_REF_COUNT,
            },
        )

    def native_call(self) -> NativeCallCode:
        return NativeCallCode(
            main_template=self.__get_template("native_call"),
            secondary_template=self.__get_decrease_ref_count_template(),
            main_data={
                "type": self.__symbols.OBJECT_TYPE,
                "arg_type": self.__symbols.NATIVE_ARGUMENT_TYPE,
                "calling_func": self.__symbols.NATIVE_CALL,
            },
            secondary_data={
                "func": self.__symbols.DECREASE_REF_COUNT,
            },
        )

    def lambda_definition(self) -> FunctionDefinitionCode:
        return self.__function_definition(self.__symbols.LAMBDA_PARAMS)

    def evaluable_definition(self) -> FunctionDefinitionCode:
        return self.__function_definition(self.__symbols.EVALUABLE_PARAMS)

    def loop(self) -> LoopCode:
        return LoopCode(
            main_template=self.__get_template("loop"),
            secondary_template=self.__get_decrease_ref_count_template(),
            main_data={
                "type": self.__symbols.OBJECT_TYPE,
            },
            secondary_data={
                "func": self.__symbols.DECREASE_REF_COUNT,
            },
        )

    def get_boolean_value(self) -> GetBooleanValueCode:
        return GetBooleanValueCode(
            main_template=self.__get_template("get_boolean_value"),
            main_data={"type": self.__symbols.BOOLEAN_TYPE, "func": self.__symbols.OBJECT_TO_BOOLEAN},
        )

    def move_environment(self) -> MoveEnvironmentCode:
        return MoveEnvironmentCode(
            main_template=self.__get_template("move_environment"),
            main_data={"func": self.__symbols.MOVE_ENVIRONMENT}
        )

    def program(self) -> ProgramCode:
        return ProgramCode(
            main_template=self.__get_template("program"),
        )

    def __lambda_call(self, main_func: str) -> LambdaCallCode:
        return LambdaCallCode(
            main_template=self.__get_template("lambda_call"),
            secondary_template=self.__get_decrease_ref_count_template(),
            main_data={
                "type": self.__symbols.OBJECT_TYPE,
                "args_type": self.__symbols.OBJECT_TYPE,
                "func": main_func,
            },
            secondary_data={
                "func": self.__symbols.DECREASE_REF_COUNT,
            },
        )

    def __make_primitive(self, main_func: str) -> MakePrimitiveCode:
        return MakePrimitiveCode(
            main_template=self.__get_template("make_primitive"),
            secondary_template=self.__get_decrease_ref_count_template(),
            main_data={
                "type": self.__symbols.OBJECT_TYPE,
                "func": main_func,
            },
            secondary_data={
                "func": self.__symbols.DECREASE_REF_COUNT,
            },
        )

    def __function_definition(self, params: str) -> FunctionDefinitionCode:
        return FunctionDefinitionCode(
            main_template=self.__get_template("function_definition"),
            main_data={
                "ret_type": self.__symbols.OBJECT_TYPE,
                "params": params,
            },
        )

    def __make_callable(self, creation_func: str) -> MakeCallableCode:
        return MakeCallableCode(
            main_template=self.__get_template("make_callable"),
            secondary_template=self.__get_decrease_ref_count_template(),
            main_data={
                "type": self.__symbols.OBJECT_TYPE,
                "creation_func": creation_func,
            },
            secondary_data={"func": self.__symbols.DECREASE_REF_COUNT},
        )

    def __get_decrease_ref_count_template(self) -> Template:
        return self.__get_template("decrease_ref_count")

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
