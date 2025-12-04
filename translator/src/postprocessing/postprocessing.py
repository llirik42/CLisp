from .context import PostprocessingContext
from .lines import Lines
from .transformations import remove_body_empty_lines, remove_increase_decrease_ref_count


def postprocess(code_text: str, context: PostprocessingContext) -> Lines:
    lines = code_text.splitlines()

    transformations = [remove_body_empty_lines, remove_increase_decrease_ref_count]

    for t in transformations:
        lines = t(lines, context)

    return lines
