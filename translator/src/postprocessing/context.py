from src.rendering import CodeCreator


class PostprocessingContext:
    def __init__(self, code_creator: CodeCreator):
        self.__code_creator = code_creator

    @property
    def code_creator(self) -> CodeCreator:
        return self.__code_creator
