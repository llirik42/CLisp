from jinja2 import Template

from src.symbols import Symbols
from src.templates import Templates
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


class CodeCreator:
    def __init__(self, symbols: Symbols, templates: Templates):
        self.__symbols = symbols
        self.__templates = templates

    def empty(self) -> EmptyCode:
        return EmptyCode()

    def make_unspecified(self) -> HavingVarCode:
        return HavingVarCode(
            main_template=self.__templates.MAKE_PRIMITIVE,
            secondary_template=self.__templates.DECREASE_REF_COUNT,
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
            main_template=self.__templates.MAKE_PRIMITIVE,
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
            main_template=self.__templates.MAKE_PRIMITIVE,
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
            main_template=self.__templates.MAKE_LIST_FROM_ARRAY,
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
            main_template=self.__templates.IF,
            secondary_template=self.__get_decrease_ref_count_template(),
            main_data={"type": self.__symbols.OBJECT_TYPE, "func": self.__symbols.OBJECT_TO_BOOLEAN},
            secondary_data={"func": self.__symbols.DECREASE_REF_COUNT},
        )

    def increase_ref_count(self) -> HavingVarCode:
        return HavingVarCode(
            main_template=self.__templates.INCREASE_REF_COUNT,
            main_data={"func": self.__symbols.INCREASE_REF_COUNT},
        )

    def decrease_ref_count(self) -> HavingVarCode:
        return HavingVarCode(
            main_template=self.__templates.DECREASE_REF_COUNT,
            main_data={"func": self.__symbols.DECREASE_REF_COUNT},
        )

    def make_environment(self) -> MakeEnvironmentCode:
        return MakeEnvironmentCode(
            main_template=self.__templates.MAKE_ENVIRONMENT,
            secondary_template=self.__templates.DESTROY_ENVIRONMENT,
            main_data={
                "type": self.__symbols.ENVIRONMENT_TYPE,
                "func": self.__symbols.CREATE_ENVIRONMENT,
            },
            secondary_data={"func": self.__symbols.DESTROY_ENVIRONMENT},
        )

    def get_global_environment(self) -> HavingVarCode:
        return HavingVarCode(
            main_template=self.__templates.GET_GLOBAL_ENVIRONMENT,
            secondary_template=self.__templates.DESTROY_ENVIRONMENT,
            main_data={
                "type": self.__symbols.ENVIRONMENT_TYPE,
                "func": self.__symbols.GET_GLOBAL_ENVIRONMENT,
            },
            secondary_data={"func": self.__symbols.DESTROY_GLOBAL_ENVIRONMENT},
        )

    def get_variable_value(self) -> GetVariableValueCode:
        return GetVariableValueCode(
            main_template=self.__templates.GET_VARIABLE_VALUE,
            main_data={
                "type": self.__symbols.OBJECT_TYPE,
                "func": self.__symbols.GET_VARIABLE_VALUE,
            },
        )

    def set_variable_value(self) -> SetVariableValueCode:
        return SetVariableValueCode(
            main_template=self.__templates.SET_VARIABLE_VALUE,
            main_data={
                "type": self.__symbols.OBJECT_TYPE,
                "func": self.__symbols.SET_VARIABLE_VALUE,
            },
        )

    def update_variable_value(self) -> UpdateVariableValueCode:
        return UpdateVariableValueCode(
            main_template=self.__templates.UPDATE_VARIABLE_VALUE,
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
            main_template=self.__templates.EVALUATION,
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
            main_template=self.__templates.NATIVE_CALL,
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
            main_template=self.__templates.LOOP,
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
            main_template=self.__templates.GET_BOOLEAN_VALUE,
            main_data={"type": self.__symbols.BOOLEAN_TYPE, "func": self.__symbols.OBJECT_TO_BOOLEAN},
        )

    def move_environment(self) -> MoveEnvironmentCode:
        return MoveEnvironmentCode(
            main_template=self.__templates.MOVE_ENVIRONMENT,
            main_data={"func": self.__symbols.MOVE_ENVIRONMENT}
        )

    def program(self) -> ProgramCode:
        return ProgramCode(
            main_template=self.__templates.PROGRAM,
        )

    def __lambda_call(self, main_func: str) -> LambdaCallCode:
        return LambdaCallCode(
            main_template=self.__templates.LAMBDA_CALL,
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
            main_template=self.__templates.MAKE_PRIMITIVE,
            secondary_template=self.__templates.DECREASE_REF_COUNT,
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
            main_template=self.__templates.FUNCTION_DEFINITION,
            main_data={
                "ret_type": self.__symbols.OBJECT_TYPE,
                "params": params,
            },
        )

    def __make_callable(self, creation_func: str) -> MakeCallableCode:
        return MakeCallableCode(
            main_template=self.__templates.MAKE_CALLABLE,
            secondary_template=self.__get_decrease_ref_count_template(),
            main_data={
                "type": self.__symbols.OBJECT_TYPE,
                "creation_func": creation_func,
            },
            secondary_data={"func": self.__symbols.DECREASE_REF_COUNT},
        )

    def __get_decrease_ref_count_template(self) -> Template:
        return self.__templates.DECREASE_REF_COUNT

    def __get_template(self, name: str) -> Template:
        """
        Returns template by the given name.

        :raises KeyError: template-file not found by the name.
        """

        return self.__templates[name]

