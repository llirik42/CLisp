from src.symbols import Symbols
from src.templates import Templates
from .codes import (
    EmptyCode,
    MakeListFromArrayCode,
    MakeEnvironmentCode,
    GetVariableValueCode,
    SetVariableValueCode,
    UpdateVariableValueCode,
    ProgramCode,
    ConditionCode,
    EvaluationCode,
    NativeCallCode,
    LoopCode,
    GetBooleanValueCode,
    MoveEnvironmentCode,
)
from .codes.decrease_ref_count import DecreaseRefCountCode
from .codes.function_definition import EvaluableDefinition, LambdaDefinition
from .codes.get_global_environment import GetGlobalEnvironmentCode
from .codes.increase_ref_count import IncreaseRefCountCode
from .codes.lambda_call import ListLambdaCallCode, OrdinaryLambdaCallCode
from .codes.make_callable import MakeLambdaCode, MakeEvaluableCode
from .codes.make_false import MakeFalseCode
from .codes.make_primitive import (
    MakeIntCode,
    MakeFloatCode,
    MakeStringCode,
    MakeCharacterCode,
)
from .codes.make_true import MakeTrueCode
from .codes.make_unspecified import MakeUnspecifiedCode


class CodeCreator:
    def __init__(self, symbols: Symbols, templates: Templates):
        self.__symbols = symbols
        self.__templates = templates

    def empty(self) -> EmptyCode:
        return EmptyCode()

    def make_unspecified(self) -> MakeUnspecifiedCode:
        return MakeUnspecifiedCode(self.__symbols, self.__templates)

    def make_int(self) -> MakeIntCode:
        return MakeIntCode(self.__symbols, self.__templates)

    def make_float(self) -> MakeFloatCode:
        return MakeFloatCode(self.__symbols, self.__templates)

    def make_string(self) -> MakeStringCode:
        return MakeStringCode(self.__symbols, self.__templates)

    def make_character(self) -> MakeCharacterCode:
        return MakeCharacterCode(self.__symbols, self.__templates)

    def make_true(self) -> MakeTrueCode:
        return MakeTrueCode(self.__symbols, self.__templates)

    def make_false(self) -> MakeFalseCode:
        return MakeFalseCode(self.__symbols, self.__templates)

    def make_lambda(self) -> MakeLambdaCode:
        return MakeLambdaCode(self.__symbols, self.__templates)

    def make_evaluable(self) -> MakeEvaluableCode:
        return MakeEvaluableCode(self.__symbols, self.__templates)

    def make_list_from_array(self) -> MakeListFromArrayCode:
        return MakeListFromArrayCode(self.__symbols, self.__templates)

    def if_(self) -> ConditionCode:
        return ConditionCode(self.__symbols, self.__templates)

    def increase_ref_count(self) -> IncreaseRefCountCode:
        return IncreaseRefCountCode(self.__symbols, self.__templates)

    def decrease_ref_count(self) -> DecreaseRefCountCode:
        return DecreaseRefCountCode(self.__symbols, self.__templates)

    def make_environment(self) -> MakeEnvironmentCode:
        return MakeEnvironmentCode(self.__symbols, self.__templates)

    def get_global_environment(self) -> GetGlobalEnvironmentCode:
        return GetGlobalEnvironmentCode(self.__symbols, self.__templates)

    def get_variable_value(self) -> GetVariableValueCode:
        return GetVariableValueCode(self.__symbols, self.__templates)

    def set_variable_value(self) -> SetVariableValueCode:
        return SetVariableValueCode(self.__symbols, self.__templates)

    def update_variable_value(self) -> UpdateVariableValueCode:
        return UpdateVariableValueCode(self.__symbols, self.__templates)

    def lambda_call(self) -> OrdinaryLambdaCallCode:
        return OrdinaryLambdaCallCode(self.__symbols, self.__templates)

    def lambda_call_list(self) -> ListLambdaCallCode:
        return ListLambdaCallCode(self.__symbols, self.__templates)

    def evaluation(self) -> EvaluationCode:
        return EvaluationCode(self.__symbols, self.__templates)

    def native_call(self) -> NativeCallCode:
        return NativeCallCode(self.__symbols, self.__templates)

    def lambda_definition(self) -> LambdaDefinition:
        return LambdaDefinition(self.__symbols, self.__templates)

    def evaluable_definition(self) -> EvaluableDefinition:
        return EvaluableDefinition(self.__symbols, self.__templates)

    def loop(self) -> LoopCode:
        return LoopCode(self.__symbols, self.__templates)

    def get_boolean_value(self) -> GetBooleanValueCode:
        return GetBooleanValueCode(self.__symbols, self.__templates)

    def move_environment(self) -> MoveEnvironmentCode:
        return MoveEnvironmentCode(self.__symbols, self.__templates)

    def program(self) -> ProgramCode:
        return ProgramCode(self.__symbols, self.__templates)
