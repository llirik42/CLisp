from typing import Union

from src.code_rendering.codes.code import Code


def wrap_codes(code: Code, wrapping: Union[Code, list[Code]]) -> Code:
    """
    Function wraps start code into the wrapping and returns one final code.

    **Example**

    code::

        func11()  # main part

        func12()  # secondary part

    wrapping[0]::

        func21()  # main part

        func22()  # secondary part

    wrapping[1]::

        func31()  # main part

        func32()  # secondary part

    wrapping[2]::

        func41()  # main part

        func42()  # secondary part

    result::

        # main part
        func21()
        func31()
        func41()
        func11()

        # secondary part
        func12()
        func42()
        func32()
        func42()

    :param code: code to wrap.
    :param wrapping: wrappings for the code. Single code works as list of one element with it.
    """

    if isinstance(wrapping, Code):
        wrapping = [wrapping]

    for c in wrapping[::-1]:
        c.add_main_epilog(code.render_main())
        c.add_secondary_prolog(code.render_secondary())
        code = c

    return code


def nest_codes(codes: list[Code]) -> Code:
    """
    Function nests codes sequentially and returns one final code.

    **Example**

    codes[0]::

        func11()  # main part

        func12()  # secondary part

    codes[1]::

        func21()  # main part

        func22()  # secondary part

    codes[2]::

        func31()  # main part

        func32()  # secondary part

    codes[3]::

        func41()  # main part

        func42()  # secondary part

    result::

        # main part
        func11()
        func21()
        func31()
        func41()

        # secondary part
        func42()
        func32()
        func22()
        func12()

    :param codes: codes to nest.
    """

    reversed_codes = codes[::-1]

    code = reversed_codes[0]
    for c in reversed_codes[1:]:
        c.add_main_epilog(code.render_main())
        c.add_secondary_prolog(code.render_secondary())
        code = c

    return code


def join_codes(codes: list[Code]) -> str:
    """
    Function joins codes sequentially and returns rendered result code.

    **Example**

    codes[0]::

        func11()  # main part

        func12()  # secondary part

    codes[1]::

        func21()  # main part

        func22()  # secondary part

    codes[2]::

        func31()  # main part

        func32()  # secondary part

    codes[3]::

        func41()  # main part

        func42()  # secondary part

    result::

        func11()

        func12()
        func21()

        func22()
        func31()

        func32()
        func41()

        func42()

    :param codes: codes to join.
    """

    rendered = [c.render() for c in codes]
    return "\n".join(rendered)


def transfer_secondary(from_: Code, to_: Code) -> None:
    """
    Function moved secondary part from one code to another.

    :param from_: the code to move from.
    :param to_: the code to move to.
    """

    to_.add_secondary_prolog(from_.render_secondary())
    from_.clear_secondary()
