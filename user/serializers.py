from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "password"]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,
            }
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            msg = _("Unable to authenticate user with provided credentials")
            raise serializers.ValidationError(msg, code="authorization")
        attrs["user"] = user
        return attrs


class DetailBalanceSerializer(serializers.Serializer):
    user_balance = serializers.FloatField()
    read_only_fields = ("user_balance",)
