from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from core.models import Operation, Record
from operation.operations import execute_operation
from record import serializers
from core.pagination import CustomPagination
from rest_framework import filters


class BaseRecordViewSet(viewsets.GenericViewSet):
    """Base view with utilities for other view sets"""

    queryset = Record.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("-date")

    def get_user_balance(self):
        queryset = self.get_queryset()
        latest_record = queryset.first()

        if not latest_record:
            return settings.DEFAULT_USER_BALANCE

        return latest_record.user_balance


class RecordViewSet(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    BaseRecordViewSet,
):
    """View for create and list record API."""

    serializer_class = serializers.RecordDetailSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    __fields = [
        "id",
        "operation_response",
        "date",
        "amount",
        "operation__type",
        "user_balance",
    ]
    ordering_fields = __fields
    search_fields = __fields

    def perform_create(self, serializer):
        operation_type = serializer.validated_data.pop("operation_type")
        operation = Operation.objects.get(
            type=operation_type,
        )
        user_balance = self.get_user_balance()
        new_balance = user_balance - operation.cost
        if new_balance < 0:
            raise ValidationError(_("Insufficient user balance to perform operation."))

        operation_input = serializer.validated_data.pop("operation_input")
        operation_response = execute_operation(
            operation_type=operation_type,
            arguments=operation_input,
        )

        serializer.save(
            user=self.request.user,
            operation=operation,
            operation_response=operation_response,
            amount=operation.cost,
            user_balance=new_balance,
        )
