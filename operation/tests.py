from unittest import mock

from django.test import SimpleTestCase

from operation.commands import (
    AdditionCommand,
    DivisionCommand,
    MultiplicationCommand,
    OperationCommand,
    RandomStringCommand,
    SquareRootCommand,
    SubtractionCommand,
)
from operation.exceptions import InvalidCommandInput, RandomStringOperationException

# Create your tests here.


class OperationsCommandTests(SimpleTestCase):
    """Test the operation command base class"""

    def test_add_numbers(self):
        """Test addition command"""

        self.assertTrue(AdditionCommand().execute([2, 3, 5]), 10)

    def test_subtract_numbers(self):
        """Test subtraction command"""

        self.assertTrue(SubtractionCommand().execute([20, 3, 5]), 12)

    def test_mul_numbers(self):
        """Test multiply command"""

        self.assertTrue(MultiplicationCommand().execute([20, 3, 5]), 300)

    def test_div_numbers(self):
        """Test division command"""

        self.assertTrue(DivisionCommand().execute([20, 5, 2]), 2)

    def test_invalid_div_by_zero(self):
        """Test division command"""

        self.assertRaises(
            InvalidCommandInput,
            DivisionCommand().execute,
            [10, 0],
        )

    def test_sqrt_numbers(self):
        """Test sqrt command"""

        self.assertTrue(SquareRootCommand().execute([2]), 4142135623730951)

    def test_invalid_sqrt_input(self):
        """Test sqrt command with invalid input"""

        self.assertRaises(
            InvalidCommandInput,
            SquareRootCommand().execute,
            [10, 100],
        )

    @mock.patch("operation.commands.requests")
    def test_random_string_command(self, mock_request):
        """Test successful call to random.org external api"""

        random_str = "ahsbdajsbhd1231"
        mock_request.get().status_code = 200
        mock_request.get().text = random_str

        self.assertTrue(RandomStringCommand().execute([]), random_str)

    @mock.patch("operation.commands.requests")
    def test_random_string_command_quota_exceeded(self, mock_request):
        """Test quota exeeded call to random.org external api"""

        mock_request.get().text = ""
        mock_request.get().status_code = 503

        self.assertRaises(
            RandomStringOperationException,
            RandomStringCommand().execute,
            [],
        )

    @mock.patch("operation.commands.requests")
    def test_random_string_command_other_errors(self, mock_request):
        """Test other errors call to random.org external api"""

        mock_request.get().text = ""
        mock_request.get().status_code = 400

        self.assertRaises(
            RandomStringOperationException,
            RandomStringCommand().execute,
            [],
        )

    def test_random_string_command_invalid_input(self):
        """Test invalid input for random string command"""

        self.assertRaises(
            InvalidCommandInput,
            RandomStringCommand().execute,
            [1234],
        )
