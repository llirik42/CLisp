import json


__all__ = ["StandardElements"]


class StandardElements:
    def __init__(self, json_path: str):
        """
        Class represents a matching table: function identifier => C-function. The identifier can be, for example, the name of a Lisp-function.

        :param json_path: path to the table in jSON format.
        :raises FileNotFoundError: file not found.
        :raises json.decoder.JSONDecodeError: file is invalid.
        """

        self.__data = json.load(open(json_path))

    def get_internal(self, identifier: str) -> str:
        # TODO: handle errors

        return self.__data["internal"][identifier]

    def get_epi_element(self, identifier: str) -> str:
        res = self.__data["api"]["functions"].get(identifier, None) or self.__data[
            "api"
        ]["macros"].get(identifier, None)

        if res is None:
            raise ValueError(
                f'Couldn\'t find function/macros by identifier "{identifier}"'
            )

        return res

    def get_function_items(self) -> list[tuple[str, str]]:
        funcs = self.__data["api"]["functions"]

        return list(funcs.items())

    @property
    def function_count(self) -> int:
        return len(self.__data["api"]["functions"])

    def get_function(self, identifier: str) -> str:
        return self.__data["functions"][identifier]

    def get_c_func(self, identifier: str) -> str:
        """
        Returns name of a C-function matching the identifier.

        :param identifier: function identifier.
        :raises ValueError: function not found.
        """

        res = self.__data.get(identifier, None)

        if res is None:
            raise ValueError(
                f'Couldn\'t find function by identifier "{identifier}" not found'
            )

        return res

    def has_identifier(self, identifier: str) -> bool:
        """
        Returns whether table has an identifier.

        :param identifier: function identifier.
        """

        return identifier in self.__data

    def get_table(self) -> dict:
        return self.__data
