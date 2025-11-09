import json
from typing import Optional


__all__ = ["ProcedureTable"]


class ProcedureTable:
    def __init__(self, json_path: str):
        """
        Class represents a matching table: Lisp-procedure => C-function.

        :param json_path: path to the table in jSON format.
        :raises FileNotFoundError: file not found.
        :raises json.decoder.JSONDecodeError: file is invalid.
        """

        self.__table = json.load(open(json_path))

    def get_c_func(self, lisp_name: str) -> Optional[str]:
        """
        Returns name of a C-function matching the Lisp-procedure or None if it doesn't exist.

        :param lisp_name: name of the Lisp-procedure.
        """

        return self.__table.get(lisp_name, None)
