class AlreadyExecutedException(Exception):
    """An AbstractProgram was attempted to be executed using execute_program(self) when it was already executed."""

    def __init__(self, *args):
        super().__init__(*args)
