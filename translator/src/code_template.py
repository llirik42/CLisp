from jinja2 import Environment


__all__ = ["CodeTemplate", "CodeTemplateCreator"]

class CodeTemplate:
    def __init__(self, name: str, env: Environment):
        self.__code_pre = ""
        self.__code_post = ""
        self.__data = {}
        self.__template_pre = env.get_template(name)
        self.__template_post = env.get_template("destroy.c")

    def set_indent_level(self, level: int):
        self.__data["indent_level"] = level

    def update(self, **kwargs) -> None:
        self.__data.update(kwargs)

    def add_code_pre(self, code: str):
        self.__code_pre += code

    def add_code_post(self, code: str):
        self.__code_post = code + self.__code_post

    def get_code_pre(self) -> str:
        return self.__code_pre

    def get_code_post(self) -> str:
        return self.__code_post

    def render(self) -> str:
        return self.render_pre() + self.render_post()

    def render_pre(self) -> str:
        return self.__template_pre.render(self.__data) + "\n" + self.__code_pre

    def render_post(self) -> str:
        return self.__code_post + "\n" + self.__template_post.render(self.__data)

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
