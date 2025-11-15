import json
from typing import Optional


__all__ = ["FunctionTable"]


class FunctionTable:
    def __init__(self, json_path: str):
        """
        Class represents a matching table: function identifier => C-function. The identifier can be, for example, the name of a Lisp-function.

        :param json_path: path to the table in jSON format.
        :raises FileNotFoundError: file not found.
        :raises json.decoder.JSONDecodeError: file is invalid.
        """

        self.__table = json.load(open(json_path))

    def get_c_func(self, identifier: str) -> str:
        """
        Returns name of a C-function matching the identifier.

        :param identifier: function identifier.
        :raises ValueError: function not found.
        """

        res = self.__table.get(identifier, None)

        if res is None:
            raise ValueError(
                f'Couldn\'t find function by identifier "{identifier}" not found'
            )

        return res
