import re

from .context import PostprocessingContext
from .lines import Lines


def remove_body_empty_lines(lines: Lines, ctx: PostprocessingContext) -> Lines:
    # TODO: Make the initial generation without empty lines, rather than using this transformation

    tab = "\t"
    result = []

    for l in lines:
        # Remove empty lines only in function bodies
        if tab in l and l.isspace():
            continue
        result.append(l)

    return result


def remove_increase_decrease_ref_count(
    lines: Lines, ctx: PostprocessingContext
) -> Lines:
    # TODO: Make the initial generation without increase-decrease on the same var, rather than using this transformation

    code_creator = ctx.code_creator

    increase_ref_count_code = code_creator.increase_ref_count()
    increase_ref_count_code.update_data(var=r"(.*?)")
    increase_ref_count_pattern = __escape_brackets(
        increase_ref_count_code.render().strip()
    )

    tab = "\t"
    decrease_ref_count_code = code_creator.decrease_ref_count()

    i = 0
    result = []
    while i < len(lines) - 1:
        current_line = lines[i]
        next_line = lines[i + 1]
        current_indent = current_line.count(tab)
        next_indent = next_line.count(tab)

        re_result = re.findall(increase_ref_count_pattern, current_line)
        if re_result and current_indent == next_indent:
            var = re_result[0]
            decrease_ref_count_code.update_data(var=var)
            if next_line.strip() == decrease_ref_count_code.render().strip():
                i += 2  # Skip current and next lines (increase, decrease)
                continue

        i += 1
        result.append(current_line)

    result.append(lines[-1])  # Add last line anyway

    return result


def __escape_brackets(s: str) -> str:
    s = s.replace("(", "\\(", 1)  # Escape first opening bracket
    s = s[::-1].replace(")", ")\\", 1)[::-1]  # Escape last closing bracket
    return s
