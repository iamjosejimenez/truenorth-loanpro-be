from unittest import mock

from django.test import SimpleTestCase

from operation.operations import (
    AdditionHandler,
    DivisionHandler,
    MultiplyHandler,
    RandomStringHandler,
    SquareRootHanlder,
    SubtractionHandler,
)

# Create your tests here.


class OperationsHandlerTests(SimpleTestCase):
    """Test the operation handler base class"""

    def test_add_numbers(self):
        """Test addition handler"""

        self.assertTrue(AdditionHandler().execute([2, 3, 5]), 10)

    def test_subtract_numbers(self):
        """Test subtraction handler"""

        self.assertTrue(SubtractionHandler().execute([20, 3, 5]), 12)

    def test_mul_numbers(self):
        """Test multiply handler"""

        self.assertTrue(MultiplyHandler().execute([20, 3, 5]), 300)

    def test_div_numbers(self):
        """Test division handler"""

        self.assertTrue(DivisionHandler().execute([20, 5, 2]), 2)

    def test_sqrt_numbers(self):
        """Test sqrt handler"""

        self.assertTrue(SquareRootHanlder().execute([2]), 4142135623730951)

    @mock.patch("operation.operations.requests")
    def test_random_string_handler(self, mock_request):
        """Test successful call to random.org external api"""

        random_str = "ahsbdajsbhd1231"
        mock_request.get().status_code = 200
        mock_request.get().text = random_str

        self.assertTrue(RandomStringHandler().execute(None), random_str)

    @mock.patch("operation.operations.requests")
    def test_random_string_handler_quota_exceeded(self, mock_request):
        """Test quota exeeded call to random.org external api"""

        mock_request.get().text = ""
        mock_request.get().status_code = 503

        self.assertRaises(
            RandomStringHandler.QuotaExceededException,
            RandomStringHandler().execute,
            None,
        )

    @mock.patch("operation.operations.requests")
    def test_random_string_handler_other_errors(self, mock_request):
        """Test other errors call to random.org external api"""

        mock_request.get().text = ""
        mock_request.get().status_code = 400

        self.assertRaises(
            RandomStringHandler.RandomStringOperationException,
            RandomStringHandler().execute,
            None,
        )
