from src.symbols import Symbols
from .ast_context import ASTContext
from .exceptions import VisitingException

# Library name (like "stdio"), function name (like "printf")
NativeFunctionVisitResult = tuple[str, str]


def visit_native_function(function: str, ctx: ASTContext) -> NativeFunctionVisitResult:
    visiting_ctx = ctx.ctx

    if function.count("/") != 1:
        raise VisitingException(
            "Invalid native function format, it must be <library/function>",
            visiting_ctx,
        )

    library_name, function_name = function.split("/")
    if len(library_name) == 0:
        raise VisitingException("Empty native function library", visiting_ctx)
    if len(function_name) == 0:
        raise VisitingException("Empty native function name", visiting_ctx)

    return library_name, function_name


def visit_native_function_types(
    types: list[str], symbols: Symbols, ctx: ASTContext
) -> list[str]:
    visiting_ctx = ctx.ctx

    result = []

    for t in types:
        native_type = symbols.try_find_native_type(t)

        if native_type:
            result.append(native_type)
            continue

        raise VisitingException(f'Native type "{t}" is not supported"', visiting_ctx)

    return result
