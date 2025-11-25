import argparse

from src.ast_reading import read_ast_file, read_ast_stdin
from src.ast_visiting import ASTVisitor
from src.rendering import CodeCreator
from src.symbols import Symbols


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
    parser.add_argument("-p", "--procedure-table", default="symbols.json")
    parser.add_argument("-t", "--templates", default="code_templates")
    args = parser.parse_args()

    ast = read_ast_stdin() if args.input_stdin else read_ast_file(args.input_file)

    standard_elements = Symbols(args.procedure_table)
    code_creator = CodeCreator(standard_elements, args.templates)

    visitor = ASTVisitor(
        symbols=standard_elements,
        code_creator=code_creator,
    )

    output_code = visitor.visit(ast)
    write_generated_code(args.output_file, output_code)


if __name__ == "__main__":
    main()
