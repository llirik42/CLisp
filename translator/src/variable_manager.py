class VariableManager:
    def __init__(self):
        self.__variable_number = 0

    def create_variable_name(self) -> str:
        self.__variable_number += 1
        return f"var{self.__variable_number}"
