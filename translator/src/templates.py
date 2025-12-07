import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template


class Templates:
    def __init__(self, templates_folder_path: str):
        self.__load_templates(templates_folder_path)

        self.MAKE_PRIMITIVE = self.__get_template("make_primitive")
        self.MAKE_LIST_FROM_ARRAY = self.__get_template("make_list_from_array")
        self.IF = self.__get_template("if")
        self.INCREASE_REF_COUNT = self.__get_template("increase_ref_count")
        self.DECREASE_REF_COUNT = self.__get_template("decrease_ref_count")
        self.MAKE_ENVIRONMENT = self.__get_template("make_environment")
        self.DESTROY_ENVIRONMENT = self.__get_template("destroy_environment")
        self.GET_GLOBAL_ENVIRONMENT = self.__get_template("get_global_environment")
        self.GET_VARIABLE_VALUE = self.__get_template("get_variable_value")
        self.SET_VARIABLE_VALUE = self.__get_template("set_variable_value")
        self.UPDATE_VARIABLE_VALUE = self.__get_template("update_variable_value")
        self.EVALUATION = self.__get_template("evaluation")
        self.NATIVE_CALL = self.__get_template("native_call")
        self.LOOP = self.__get_template("loop")
        self.GET_BOOLEAN_VALUE = self.__get_template("get_boolean_value")
        self.MOVE_ENVIRONMENT = self.__get_template("move_environment")
        self.PROGRAM = self.__get_template("program")
        self.LAMBDA_CALL = self.__get_template("lambda_call")
        self.FUNCTION_DEFINITION = self.__get_template("function_definition")
        self.MAKE_CALLABLE = self.__get_template("make_callable")

    def __get_template(self, name: str) -> Template:
        return self.__templates[name]

    def __load_templates(self, templates_folder_path: str) -> None:
        env = Environment(loader=FileSystemLoader(templates_folder_path))

        self.__templates = {
            Path(name).stem: env.get_template(name)
            for name in os.listdir(templates_folder_path)
        }
