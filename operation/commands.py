"""
    Module with implementation details for every operation supported by the platform.
    Its design followed the command pattern, in order to have a class for every operation,
    while having a parent class which defines common behaviour.
"""
import math
from abc import ABC
from functools import reduce
from typing import List

import requests

from core.models import Operation
from operation.exceptions import InvalidCommandInput, RandomStringOperationException


class OperationCommand(ABC):
    """Base abstract class for operation handlers"""

    def execute():
        pass


class AdditionCommand(OperationCommand):
    """Addition implementation command"""

    def execute(self, arguments):
        return sum(arguments)


class SubtractionCommand(OperationCommand):
    """Subtraction implementation command"""

    def execute(self, arguments):
        return reduce(lambda x, y: x - y, arguments)


class MultiplicationCommand(OperationCommand):
    """Addition implementation command"""

    def execute(self, arguments):
        return math.prod(arguments)


class DivisionCommand(OperationCommand):
    """Division implementation command"""

    def execute(self, arguments: List[float]):
        if len(arguments) < 2:
            raise InvalidCommandInput("Divison operation needs at least to operands")

        for argument in arguments[1:]:
            if argument == 0:
                raise InvalidCommandInput("Divison by zero not supported")

        return reduce(lambda x, y: x / y, arguments)


class SquareRootCommand(OperationCommand):
    """Square root command implementation details"""

    def execute(self, arguments):
        if len(arguments) != 1:
            raise InvalidCommandInput("SQRT operation only takes 1 argument")

        return math.sqrt(arguments[0])


class RandomStringCommand(OperationCommand):
    """Random string generation operation command"""

    def execute(self, arguments):
        """Make request to external service"""

        if len(arguments):
            raise InvalidCommandInput("Random String operation takes 0 arguments")

        # It's best to extract this value from env vairables.
        base_url = "https://www.random.org/strings/"
        params = {
            "num": 1,
            "len": 8,
            "digits": "on",
            "upperalpha": "on",
            "loweralpha": "on",
            "unique": "on",
            "format": "plain",
            "rnd": "new",
        }

        response = requests.get(base_url, params=params)
        response_content = response.text.strip()
        if response.status_code == 200:
            return response_content

        if response.status_code == 503:
            raise RandomStringOperationException("External service quota exceeded")

        raise RandomStringOperationException(response_content)


OPERATION_TYPE_2_HANDLER = {
    Operation.OperationType.ADDITION: AdditionCommand,
    Operation.OperationType.SUBTRACTION: SubtractionCommand,
    Operation.OperationType.MULTIPLICATION: MultiplicationCommand,
    Operation.OperationType.DIVISION: DivisionCommand,
    Operation.OperationType.SQUARE_ROOT: SquareRootCommand,
    Operation.OperationType.RANDOM_STRING: RandomStringCommand,
}


def execute_operation(operation_type, arguments):
    """Helper method to execute operation type and return a response"""
    return OPERATION_TYPE_2_HANDLER[operation_type]().execute(arguments)
