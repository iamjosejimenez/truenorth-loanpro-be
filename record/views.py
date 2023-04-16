from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Operation, Record
from operation.operations import execute_operation
from record import serializers


# Create your views here.
class RecordViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """View for create record API."""

    serializer_class = serializers.RecordDetailSerializer
    queryset = Record.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        operation_type = serializer.validated_data.pop("operation_type")
        operation = Operation.objects.get(
            type=operation_type,
        )

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
            user_balance=0.0,
        )
