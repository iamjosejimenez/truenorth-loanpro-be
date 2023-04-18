from rest_framework import serializers

from core.models import Operation


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ("type",)
