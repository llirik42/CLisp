class VariableManager:
    def __init__(self):
        """
        Class is responsible for creating names for the variables.
        """

        self.__object_count = 0
        self.__environment_count = -1
        self.__lambda_count = 0
        self.__evaluable_count = 0

    def create_object_name(self) -> str:
        """
        Creates and returns a name of the variable for the new object.
        """

        self.__object_count += 1
        return f"var{self.__object_count}"

    def create_environment_name(self) -> str:
        """
        Creates and returns a name of the variable with a new environment.
        """

        self.__environment_count += 1

        if self.__environment_count == 0:
            return "global_env"

        return f"env{self.__environment_count}"

    def create_lambda_function_name(self) -> str:
        """
        Creates and returns a name of the function of a lambda.
        """

        self.__lambda_count += 1

        return f"lambda{self.__lambda_count}"

    def create_evaluable_function_name(self) -> str:
        """
        Creates and returns a name of the function of an evaluable.
        """

        self.__evaluable_count += 1

        return f"evaluable{self.__evaluable_count}"
