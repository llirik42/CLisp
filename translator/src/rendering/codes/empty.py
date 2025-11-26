from .code import Code


class EmptyCode(Code):
    def __init__(self):
        super().__init__()
        self.remove_newlines()
