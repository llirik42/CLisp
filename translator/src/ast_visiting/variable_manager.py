class VariableManager:
    def __init__(self):
        """
        Class is responsible for creating names for the variables.
        """

        self.__variable_number = 0

    def create_variable_name(self) -> str:
        """
        Creates and returns a name for a new variable.
        """

        self.__variable_number += 1
        return f"var{self.__variable_number}"
