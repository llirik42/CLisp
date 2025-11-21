__all__ = ["VariableManager"]


class VariableManager:
    def __init__(self):
        """
        Class is responsible for creating names for the variables.
        """

        self.__object_count = 0
        self.__environment_count = -1
        self.__function_count = 0

    def create_object_name(self) -> str:
        """
        Creates and returns a name of the variable with a new object.
        """

        self.__object_count += 1

        return f"var{self.__object_count}"

    def create_environment_name(self) -> str:
        """
        Creates and returns a name of the variable with a new environment
        """

        self.__environment_count += 1

        if self.__environment_count == 0:
            return "global_env"

        return f"env{self.__environment_count}"

    def create_function_name(self) -> str:
        """
        Creates and returns a name of the function of a lambda.
        """

        self.__function_count += 1

        return f"func{self.__function_count}"
