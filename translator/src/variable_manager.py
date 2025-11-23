__all__ = ["VariableManager"]


class VariableManager:
    def __init__(self):
        """
        Class is responsible for creating names for the variables.
        """

        self.__object_count = 0
        self.__environment_count = -1
        self.__function_count = 0

        self.__function = False
        self.__function_object_count = 0

    def reset_object_count(self):
        self.__object_count = 0

    def create_object_name(self) -> str:
        """
        Creates and returns a name of the variable with a new object.
        """

        if not self.__function:
            self.__object_count += 1
            return f"var{self.__object_count}"

        self.__function_object_count += 1
        return f"var{self.__function_object_count}"

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

    def enter_function(self) -> None:
        self.__function = True
        self.__function_object_count = 0

    def exit_function(self) -> None:
        self.__function = False

    @property
    def object_count(self) -> int:
        return self.__function_object_count
