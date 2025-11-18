__all__ = ["VariableManager"]


class VariableManager:
    def __init__(self):
        """
        Class is responsible for creating names for the variables.
        """

        self.__objects_count = 0
        self.__environments_count = 0

    def create_object_name(self) -> str:
        """
        Creates and returns a name of the variable with a new object.
        """

        self.__objects_count += 1
        return f"var{self.__objects_count}"

    def create_environment_name(self) -> str:
        """
        Creates and returns a name of the variable with a new environment
        """

        self.__environments_count += 1
        return f"env{self.__environments_count}"
