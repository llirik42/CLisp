from .code import Code

# TODO: сделать лишь один параметр - список кодов (изменить документацию)
def wrap_codes(codes: list[Code]) -> Code:
    """
    Function wraps start code into the wrapping ones.

    **Example**

    start code::

        func11()  # main part

        func12()  # secondary part

    wrapping code[0]::

        func21()  # main part

        func22()  # secondary part

    wrapping code[1]::

        func31()  # main part

        func32()  # secondary part

    result::

        # main part
        func11()
        func21()
        func31()

        # secondary part
        func32()
        func22()
        func12()
    """

    code = codes[0]

    for c in codes[:0:-1]:
        c.add_main_epilog(code.render_main())
        c.add_secondary_prolog(code.render_secondary())
        code = c

    return code


def nest_codes(codes: list[Code]) -> Code:
    # TODO: add pydoc

    reversed_codes = codes[::-1]

    code = reversed_codes[0]
    for c in reversed_codes[1:]:
        c.add_main_epilog(code.render_main())
        c.add_secondary_prolog(code.render_secondary())
        code = c

    return code


def join_codes(codes: list[Code]) -> str:
    rendered = [c.render() for c in codes]
    return "\n".join(rendered)


def transfer_secondary(from_: Code, to_: Code) -> None:
    to_.add_secondary_prolog(from_.render_secondary())
    from_.clear_secondary()

