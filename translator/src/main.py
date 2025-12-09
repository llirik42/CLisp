import argparse
import sys

from src.ast_reading import read_ast
from src.ast_visiting import ASTVisitor
from src.postprocessing import postprocess, PostprocessingContext
from src.preprocessing import preprocess
from src.rendering import CodeCreator
from src.source_reading import read_from_stdin, read_from_file
from src.symbols import Symbols
from src.templates import Templates


def write_generated_code(code_lines: list[str], output_file: str) -> None:
    """
    Writes generated code to the given file.

    :param code_lines: lines of code to write.
    :param output_file: path to the file to write.
    """

    # It doesn't write empty lines in the bodies
    with open(output_file, "w") as f:
        for l in code_lines:
            f.write(l + "\n")


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
    parser.add_argument("-s", "--symbols-table", default="symbols.json")
    parser.add_argument("-t", "--templates", default="code_templates")
    args = parser.parse_args()

    source = read_from_stdin() if args.input_stdin else read_from_file(args.input_file)
    read_ast(source)  # So syntax errors will be detected and printed with correct lines number

    preprocessed = preprocess(source)
    ast = read_ast(preprocessed)

    symbols = Symbols(args.symbols_table)
    templates = Templates(args.templates)

    code_creator = CodeCreator(symbols, templates)

    visitor = ASTVisitor(
        symbols=symbols,
        code_creator=code_creator,
    )
    code_text = visitor.visit(ast)

    preprocessing_context = PostprocessingContext(code_creator)
    preprocessed_code_lines = postprocess(code_text, preprocessing_context)

    write_generated_code(preprocessed_code_lines, args.output_file)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        curr_e = e
        while curr_e:
            print(curr_e, file=sys.stderr)
            curr_e = curr_e.__cause__
        exit(1)
