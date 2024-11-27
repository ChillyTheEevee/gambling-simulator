class ExecutionNotInitiatedException(Exception):
    """A continuation method of AbstractMethod was called without first initiating execution."""

    def __init__(self, *args):
        super().__init__(*args)
