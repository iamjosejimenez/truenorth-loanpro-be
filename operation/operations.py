import math
from abc import ABC
from functools import reduce

import requests

from core.models import Operation


class OperationHandler(ABC):
    def execute():
        pass


class AdditionHandler(OperationHandler):
    def execute(self, arguments):
        return sum(arguments)


class SubtractionHandler(OperationHandler):
    def execute(self, arguments):
        return reduce(lambda x, y: x - y, arguments)


class MultiplyHandler(OperationHandler):
    def execute(self, arguments):
        return math.prod(arguments)


class DivisionHandler(OperationHandler):
    def execute(self, arguments):
        return reduce(lambda x, y: x / y, arguments)


class SquareRootHanlder(OperationHandler):
    def execute(self, arguments):
        return math.sqrt(arguments[0])


class RandomStringHandler(OperationHandler):
    """Random string generation operation"""

    class RandomStringOperationException(Exception):
        """Exception raised when external service's quota is exceeded"""

        def __init__(self, message="External service quota exceeded") -> None:
            self.message = message
            super().__init__(self.message)

    class QuotaExceededException(Exception):
        """Exception raised when external service's quota is exceeded"""

        def __init__(self, message="External service quota exceeded") -> None:
            self.message = message
            super().__init__(self.message)

    def execute(self, _arguments):
        """Make request to external service"""

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
            raise RandomStringHandler.QuotaExceededException()

        raise RandomStringHandler.RandomStringOperationException(response_content)


OPERATION_TYPE_2_HANDLER = {
    Operation.OperationType.ADDITION: AdditionHandler,
    Operation.OperationType.SUBTRACTION: SubtractionHandler,
    Operation.OperationType.MULTIPLICATION: MultiplyHandler,
    Operation.OperationType.DIVISION: DivisionHandler,
    Operation.OperationType.SQUARE_ROOT: SquareRootHanlder,
    Operation.OperationType.RANDOM_STRING: RandomStringHandler,
}


def execute_operation(operation_type, arguments):
    """Helper method to execute operation type and return a response"""
    return OPERATION_TYPE_2_HANDLER[operation_type]().execute(arguments)
