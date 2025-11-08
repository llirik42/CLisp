import argparse

from antlr4 import *
from jinja2 import Environment, FileSystemLoader

from LispLexer import LispLexer
from LispParser import LispParser
from ast_visitor import ASTVisitor
from procedures import read_procedure_table
from src.code_template import CodeTemplateCreator


def read_ast(input_file: str):
    input_stream = FileStream(input_file)
    lexer = LispLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LispParser(stream)
    return parser.program()


def write_generated_code(output_file: str, code: str) -> None:
    open(output_file, "w").write(code)


def main():
    parser = argparse.ArgumentParser(
        prog="CLisp translator", description="Generates C-code from Lisp-code"
    )
    parser.add_argument("filename")
    parser.add_argument("-o", "--output-file", required=False)
    parser.add_argument("-p", "--procedure-table", required=False)
    parser.add_argument("-t", "--templates", required=False)
    args = parser.parse_args()

    input_file_path = args.filename
    output_file_path = args.output_file or "output.c"
    procedure_table_path = args.procedure_table or "procedure_table.json"
    templates_folder_path = args.templates or "templates"

    template_env = Environment(loader=FileSystemLoader(templates_folder_path))
    template_creator = CodeTemplateCreator(template_env)
    procedure_table = read_procedure_table(procedure_table_path)
    ast = read_ast(input_file_path)
    visitor = ASTVisitor(procedure_table, template_creator)
    output_code = visitor.visit(ast)
    write_generated_code(output_file_path, output_code)


if __name__ == "__main__":
    main()
