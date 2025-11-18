import argparse

from src.environment import EnvironmentContext
from src.evaluable_context import EvaluableContext
from .ast_visiting import ASTVisitor
from .code_rendering import CodeCreator
from .function_table import FunctionTable
from .ast_reading import read_ast_file
from src.variable_manager import VariableManager


def write_generated_code(output_file: str, code: str) -> None:
    """
    Writes generated code to the given file.

    :param output_file: path to the file to write.
    :param code: code to file to write.
    """

    open(output_file, "w").write(code)


def main():
    parser = argparse.ArgumentParser(
        prog="CLisp translator", description="Generates C-code from Lisp-code."
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "-i", "--input_stdin", action="store_true", help="Read Lisp-code from stdin"
    )
    input_group.add_argument(
        "-f", "--input_file", action="store", help="Read Lisp-Code from the file"
    )
    parser.add_argument("-o", "--output-file", default="output.c")
    parser.add_argument("-p", "--procedure-table", default="function_table.json")
    parser.add_argument("-t", "--templates", default="code_templates")
    args = parser.parse_args()

    code_creator = CodeCreator(args.templates)
    function_table = FunctionTable(args.procedure_table)

    l1 = ["1.scm", "2.scm"]
    l2 = ["1_actual.c", "2_actual.c"]

    assert len(l1) == len(l2)

    for i in range(len(l1)):
        visitor = ASTVisitor(
            function_table=function_table,
            code_creator=code_creator,
            variable_manager=VariableManager(),
            evaluable_context=EvaluableContext(),
            environment_context=EnvironmentContext(),
        )

        f_in = l1[i]
        ast = read_ast_file(f_in)
        output_code = visitor.visit(ast)
        write_generated_code(l2[i], output_code)

        output_code = output_code.split("\n")

        with open(f"{i+1}.c", "r") as f:
            expected_code = f.read().split("\n")

        line = 0
        while True:
            if output_code[line].strip() != expected_code[line].strip():
                print(f"File {i+1}, line {line + 1} !!!")
                break

            line += 1

            if line >= max(len(expected_code), len(output_code)):
                print(f"{i+1}.scm is OK!")

                break


if __name__ == "__main__":
    main()
