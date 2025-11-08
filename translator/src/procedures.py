import json
from typing import Optional

__all__ = ["ProcedureTable", "read_procedure_table", "add_procedure", "get_c_name"]

ProcedureTable = dict[str, str]


def read_procedure_table(path: str) -> ProcedureTable:
    return json.load(open(path))


def add_procedure(table: ProcedureTable, lisp_name: str, c_name: str) -> None:
    table[lisp_name] = c_name


def get_c_name(table: ProcedureTable, lisp_name: str) -> Optional[str]:
    return table.get(lisp_name, None)
