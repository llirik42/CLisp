import argparse


from ast_visitor import ASTVisitor
from code_rendering import CodeCreator
from procedure_table import ProcedureTable
from ast_reading import read_ast


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
    parser.add_argument("input_file")
    parser.add_argument("-o", "--output-file", required=False)
    parser.add_argument("-p", "--procedure-table", required=False)
    parser.add_argument("-t", "--templates", required=False)
    args = parser.parse_args()

    input_file_path = args.input_file
    output_file_path = args.output_file or "output.c"
    procedure_table_path = args.procedure_table or "procedure_table.json"
    templates_folder_path = args.templates or "code_templates"

    ast = read_ast(input_file_path)
    code_creator = CodeCreator(templates_folder_path)
    procedure_table = ProcedureTable(procedure_table_path)
    visitor = ASTVisitor(procedure_table, code_creator)

    output_code = visitor.visit(ast)
    write_generated_code(output_file_path, output_code)


if __name__ == "__main__":
    main()
