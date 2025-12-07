import json
from typing import Optional, Any

__all__ = ["Symbols"]


SymbolSection = dict[str, Any]


class Symbols:
    def __init__(self, json_path: str):
        """
        The class contains symbols that are used in code generating. Every symbol is a pair: (identifier, symbol). The identifier can be, for example, the name of a Lisp-function and symbol can then will be the name of a C-function that implements Lisp-function. All symbols are divided into sections:

        * API
        * internals

        API contains symbols that can be used in Lisp-code, while internals are used only in code generating and their symbols is not supported in Lisp-code.

        :param json_path: path to the table in jSON format.
        :raises FileNotFoundError: file not found.
        :raises json.decoder.JSONDecodeError: file is invalid.
        """

        self.__data = json.load(open(json_path))

        self.BOOLEAN_TYPE = self.__find_internal("boolean_type")
        self.OBJECT_TYPE = self.__find_internal("object_type")
        self.ENVIRONMENT_TYPE = self.__find_internal("environment_type")
        self.NATIVE_ARGUMENT_TYPE = self.__find_internal("native_argument_type")
        self.CREATE_UNSPECIFIED = self.__find_internal("unspecified")
        self.CREATE_INTEGER = self.__find_internal("integer")
        self.CREATE_FLOAT = self.__find_internal("float")
        self.CREATE_STRING = self.__find_internal("string")
        self.CREATE_CHARACTER = self.__find_internal("character")
        self.CREATE_TRUE = self.__find_internal("true")
        self.CREATE_FALSE = self.__find_internal("false")
        self.CREATE_LAMBDA = self.__find_internal("lambda")
        self.CREATE_EVALUABLE = self.__find_internal("evaluable")
        self.CREATE_LIST = self.__find_internal("list")
        self.CREATE_LIST_FROM_ARRAY = self.__find_internal("list_array")
        self.OBJECT_TO_BOOLEAN = self.__find_internal("to_boolean")
        self.CREATE_ENVIRONMENT = self.__find_internal("environment")
        self.MOVE_ENVIRONMENT = self.__find_internal("move_environment")
        self.DESTROY_ENVIRONMENT = self.__find_internal("~environment")
        self.GET_GLOBAL_ENVIRONMENT = self.__find_internal("environment_global")
        self.DESTROY_GLOBAL_ENVIRONMENT = self.__find_internal("~environment_global")
        self.GET_VARIABLE_VALUE = self.__find_internal("get_variable_value")
        self.SET_VARIABLE_VALUE = self.__find_internal("set_variable_value")
        self.UPDATE_VARIABLE_VALUE = self.__find_internal("update_variable_value")
        self.CALL_LAMBDA = self.__find_internal("lambda_call")
        self.CALL_LAMBDA_LIST = self.__find_internal("lambda_call_list")
        self.EVALUATE = self.__find_internal("evaluation")
        self.NATIVE_CALL = self.__find_internal("native_call")
        self.INCREASE_REF_COUNT = self.__find_internal("ref_count++")
        self.DECREASE_REF_COUNT = self.__find_internal("ref_count--")
        self.LAMBDA_PARAMS = self.__find_internal("lambda_function_params")
        self.LAMBDA_ENV = self.__find_internal("lambda_env")
        self.LAMBDA_ARGS = self.__find_internal("lambda_args")
        self.LAMBDA_COUNT = self.__find_internal("lambda_count")
        self.EVALUABLE_PARAMS = self.__find_internal("evaluable_function_params")
        self.EVALUABLE_ENV = self.__find_internal("evaluable_env")

    def try_find_native_type(self, identifier: str) -> Optional[str]:
        """
        Finds and returns the symbol that matches a native type.

        :param identifier: identifier of a symbol.
        :return: found symbol or None.
        """

        return self.__native_types.get(identifier, None)

    def get_api_function_items(self) -> list[tuple[str, str]]:
        """
        Returns all symbols from API functions as pairs: (identifier, symbol).

        :return: list of the symbols as pairs.
        """

        return list(self.__api_functions.items())

    def has_api_function_symbol(self, identifier: str) -> bool:
        """
        Returns whether there is an API symbol.

        :param identifier: identifier of a symbol.
        :return: True if there is an API symbol.
        """

        return identifier in self.__api_functions

    def __find_internal(self, identifier: str) -> str:
        return self.__internal[identifier]

    @property
    def __native_types(self) -> SymbolSection:
        return self.__api["native_types"]

    @property
    def __api_functions(self) -> SymbolSection:
        return self.__api["functions"]

    @property
    def __api(self) -> SymbolSection:
        return self.__data["api"]

    @property
    def __internal(self) -> SymbolSection:
        res = {}

        for v in self.__data["internal"].values():
            res.update(v)

        return res
