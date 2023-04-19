from rest_framework.exceptions import APIException


class InvalidOperationApiException(APIException):
    """API exception to handle errors in operations"""

    status_code = 400
    default_detail = "Invalid operation"
    default_code = "invalid_operation"

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
