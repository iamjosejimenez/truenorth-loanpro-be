from rest_framework import serializers

from core.models import Operation, Record
from operation.serializers import OperationSerializer


class RecordDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = (
            "id",
            "operation_response",
            "date",
            "user_balance",
            "amount",
            "operation_type",
            "operation_input",
            "operation",
        )
        read_only_fields = (
            "id",
            "operation_response",
            "date",
            "user_balance",
            "amount",
            "operation",
        )

    operation_type = serializers.ChoiceField(
        choices=Operation.OperationType.choices,
        write_only=True,
    )

    operation_input = serializers.ListField(
        child=serializers.FloatField(),
        write_only=True,
        max_length=2,
    )

    operation = OperationSerializer(read_only=True)
