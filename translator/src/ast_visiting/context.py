class ConditionVisitingContext:
    def __init__(self):
        self.__counter = 0

    def __enter__(self):
        self.__counter += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__counter -= 1

    @property
    def visiting(self):
        return self.__counter > 0
