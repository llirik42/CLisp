import json
from typing import Optional


__all__ = ["Symbols"]


SymbolSection = dict[str, str]


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

    def find_internal(self, identifier: str) -> str:
        """
        Finds and returns the symbol from the internals.

        :param identifier: identifier of a symbol.
        :return: found symbol or None.
        """

        return self.__internal[identifier]

    def find_api_symbol(self, identifier: str) -> Optional[str]:
        """
        Finds and returns the symbol from the API.

        :param identifier: identifier of a symbol.
        :return: found symbol or None.
        """

        return self.__api.get(identifier, None)

    def find_api_function_items(self) -> list[tuple[str, str]]:
        """
        Returns all symbols from API functions as pairs: (identifier, symbol).

        :return: list of the symbols as pairs.
        """

        return list(self.__api.items())

    def has_api_symbol(self, identifier: str) -> bool:
        """
        Returns whether there is an API symbol.

        :param identifier: identifier of a symbol.
        :return: True if there is an API symbol.
        """

        return self.find_api_symbol(identifier) is not None

    @property
    def __api(self) -> SymbolSection:
        return self.__data["api"]

    @property
    def __internal(self) -> SymbolSection:
        return self.__data["internal"]
