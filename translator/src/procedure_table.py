import json
from typing import Optional

__all__ = ["ProcedureTable"]


class ProcedureTable:
    def __init__(self, path: str):
        self.__table = json.load(open(path))

    def get_c_name(self, lisp_name: str) -> Optional[str]:
        return self.__table.get(lisp_name, None)
