from src.code_rendering import Code
from dataclasses import dataclass


@dataclass()
class Environment:
    name: str
    code: Code
    variables: dict[str, str]
    parent: "Environment"

    @property
    def has_parent(self) -> bool:
        return self.parent is not None

