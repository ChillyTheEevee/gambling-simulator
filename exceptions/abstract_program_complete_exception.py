class AbstractProgramCompleteException(Exception):
    """An AbstractProgram was attempted to be executed when it already completed execution."""

    def __init__(self, *args):
        super().__init__(*args)
