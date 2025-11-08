from jinja2 import Environment


__all__ = ["CodeTemplate", "CodeTemplateCreator"]

class CodeTemplate:
    def __init__(self, name: str, env: Environment):
        self.__data = {}
        self.__template = env.get_template(name)

    def update(self, **kwargs) -> None:
        self.__data.update(kwargs)

    def update_code(self, code: str) -> None:
        self.__data.update({"code": code})

    def render(self) -> str:
        return self.__template.render(self.__data)


class CodeTemplateCreator:
    def __init__(self, env: Environment):
        self.__env = env

    def make_int(self) -> CodeTemplate:
        return CodeTemplate("make_integer.c", self.__env)

    def make_string(self) -> CodeTemplate:
        return CodeTemplate("make_string.c", self.__env)

    def make_boolean(self) -> CodeTemplate:
        return CodeTemplate("make_boolean.c", self.__env)

    def procedure_call(self) -> CodeTemplate:
        return CodeTemplate("procedure_call.c", self.__env)
