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

    def has_variable(self, variable: str) -> bool:
        return variable in self.variables

    def has_variable_recursively(self, name: str) -> bool:
        if self.has_variable(name):
            return True

        if self.has_parent:
            return _has_variable_recursively(self.parent, name)

        return False

    def update_variable(self, name: str, value: str) -> None:
        self.variables[name] = value

    def update_variable_recursively(self, name: str, value: str) -> None:
        if name in self.variables:
            self.variables[name] = value
            return

        if self.has_parent:
            self.parent.update_variable_recursively(name, value)
