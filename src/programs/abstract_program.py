from abc import ABC, abstractmethod

from src.exceptions.abstract_program_complete_exception import AbstractProgramCompleteException
from src.exceptions.already_executed_exception import AlreadyExecutedException
from src.exceptions.execution_not_initiated_exception import ExecutionNotInitiatedException


class AbstractProgram(ABC):
    """
    An abstract representation of a terminal program.

    AbstractPrograms are processed first with an initial call to execute_program(self) and then (if necessary) with
    sequential calls to the process_user_input(self, user_input) method. When either method is called, an
    AbstractProgram will perform all tasks up until it requires additional input from a user. Then, the driver method
    will return and the AbstractProgram will wait until process_user_input(self, user_input) is called with the
    additional input required.

    An AbstractProgram retrains its state throughout sequential calls of its methods.

    The lifecycle of an AbstractProgram is as follows:
    1). Instantiation - The AbstractProgram instantiation has been instantiated, but has not yet been called.
    2). Execution - The AbstractProgram's execute_program(self) method is called and the AbstractProgram begins
            execution. This method either returns True or False.
    3). Subsequent Calls - If False is returned from execute_program(self), the AbstractProgram requires additional
            user input to complete execution and may be continued with subsequent calls to
            process_user_input(self, user_input) until process_user_input(self, user_input) returns True.
    4). Program completion - Once either a call to execute_program(self) or process_user_input(self, user_input) returns
            True, any subsequent calls to this AbstractProgram will result in an error being thrown.
    """

    def __init__(self):
        self.execution_begun = False
        self.completed_execution = False

    def execute_program(self) -> bool:
        """
        Executes this AbstractProgram until either it has reached full completion or requires additional input. This
        method ensures state checks are consistent across implementations.

        Returns:
            bool: True if this AbstractProgram has completed execution without the need for additional input,
                False otherwise.

        Exceptions:
            AlreadyExecutedException: If this AbstractProgram has already been executed.
        """
        if self.execution_begun:
            raise AlreadyExecutedException()
        self.execution_begun = True
        completion_state = self._execute()
        self.completed_execution = completion_state
        return completion_state

    @abstractmethod
    def _execute(self) -> bool:
        """
        Subclasses must implement this method to provide specific execution logic.

        Returns:
            bool: True if this AbstractProgram has completed execution without the need for additional input,
                False otherwise.
        """
        pass

    def process_user_input(self, user_input: str) -> bool:
        """
        Continues execution of this AbstractProgram until either it has reached completion or requires additional input.

        Args:
            user_input (str): The user input

        Returns:
            bool: True if the AbstractProgram has completed execution without the need for additional input,
                False otherwise.

        Exceptions:
            AbstractProgramCompleteException: If called when this AbstractProgram has already completed execution.
            ExecutionNotInitiatedException: If called when execute_program(self) has not yet been called.
        """
        if self.completed_execution:
            raise AbstractProgramCompleteException()
        if not self.execution_begun:
            raise ExecutionNotInitiatedException()
        completion_state = self._process_input(user_input)
        self.completed_execution = completion_state
        return completion_state

    @abstractmethod
    def _process_input(self, user_input: str) -> bool:
        """
        Subclasses must implement this method to handle specific execution logic.

        Returns:
            bool: True if the AbstractProgram has completed execution without the need for additional input,
                False otherwise.
        """
        pass
