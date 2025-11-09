from jinja2 import Environment, FileSystemLoader

__all__ = ["Code", "CodeCreator"]


class Code:
    def __init__(self, name: str, env: Environment, post: bool = True):
        self.__code_pre = ""
        self.__code_post = ""
        self.__data = {}
        self.__template_pre = env.get_template(name)
        self.__template_post = env.get_template("destroy.c")
        self.__final = False
        self.__post = post

    def make_final(self):
        self.__final = True

    def update_data(self, **kwargs) -> None:
        self.__data.update(kwargs)

    def add_code_pre(self, code: str):
        self.__code_pre += code

    def add_code_post(self, code: str):
        self.__code_post = code + self.__code_post

    def render(self) -> str:
        if self.__post:
            return self.render_pre() + self.render_post()

        return self.render_pre()

    def render_pre(self) -> str:
        tmp = self.__template_pre.render(self.__data) + "\n" + self.__code_pre

        if self.__final:
            return tmp[:-1]  # remove trailing \n

        return tmp

    def render_post(self) -> str:
        tmp = self.__code_post + "\n" + self.__template_post.render(self.__data)

        if self.__final:
            return tmp + "\n"

        return tmp


class CodeCreator:
    def __init__(self, templates_folder_path: str):
        self.__env = Environment(loader=FileSystemLoader(templates_folder_path))

    def make_int(self) -> Code:
        return Code("make_integer.c", self.__env)

    def make_string(self) -> Code:
        return Code("make_string.c", self.__env)

    def make_boolean(self) -> Code:
        return Code("make_boolean.c", self.__env)

    def procedure_call(self) -> Code:
        return Code("procedure_call.c", self.__env)

    def top_level(self) -> Code:
        return Code("top_level.c", self.__env, post=False)
