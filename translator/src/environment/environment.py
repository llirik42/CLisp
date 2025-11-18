from src.code_rendering import Code
from dataclasses import dataclass


@dataclass()
class Environment:
    """
    Class represents a variable environment: list of the Lisp-variables with their C-variables names.
    """

    # C-variable in code that stores a pointer to the C-structure of the environment
    name: str

    # Code of the whole environment (creation of it, expressions in it, destroying of it)
    code: Code

    # Lisp-variable => C-variable
    variables: dict[str, str]

    # Parent environment
    parent: "Environment"

    @property
    def has_parent(self) -> bool:
        """
        Returns whether this environment has a parent one.
        """

        return self.parent is not None
