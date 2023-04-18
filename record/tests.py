from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Operation, Record
from record.serializers import RecordDetailSerializer

RECORD_URL = reverse("record:record-list")


def create_record(
    user,
    operation,
    serialized=False,
    **params,
):
    """Create and return a sample record."""
    defaults = {
        "user_balance": 10.0,
        "amount": operation.cost,
        "operation_response": 15.5,
    }
    defaults.update(params)

    record = Record.objects.create(
        operation=operation,
        user=user,
        **defaults,
    )

    if not serialized:
        return record

    return RecordDetailSerializer(record).data


class PublicRecordApiTests(TestCase):
    """Test unauthenticated API Request."""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to access record API."""
        res = self.client.get(RECORD_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PtivateRecordApiTests(TestCase):
    """Test authenticated API Request."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@example.com",
            "testpass123",
        )
        self.client.force_authenticate(self.user)
        self.operation_1 = Operation.objects.create(
            type=Operation.OperationType.ADDITION,
            cost=2.45,
        )
        self.operation_2 = Operation.objects.create(
            type=Operation.OperationType.SUBTRACTION,
            cost=3.78,
        )

    def test_retrieve_records(self):
        """Test retrieving a list of records."""

        create_record(user=self.user, operation=self.operation_1)
        create_record(user=self.user, operation=self.operation_2)

        res = self.client.get(RECORD_URL)

        records = Record.objects.all().order_by("-id")
        serializer = RecordDetailSerializer(records, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 2)
        self.assertEqual(res.data["results"], serializer.data)

    def test_record_list_limited_to_user(self):
        """Test list of records is limited to authenticated user."""

        other_user = get_user_model().objects.create_user(
            "other@example.com",
            "password123",
        )
        record_1 = create_record(
            user=other_user,
            operation=self.operation_1,
            serialized=True,
        )

        record_2 = create_record(
            user=self.user,
            operation=self.operation_1,
            serialized=True,
        )

        res = self.client.get(RECORD_URL)
        self.assertEqual(res.data["count"], 1)

        retrieved_records = res.data["results"]
        self.assertNotIn(record_1, retrieved_records)
        self.assertIn(record_2, retrieved_records)

    def test_delete_record(self):
        """Test deleting a single records."""

        record = create_record(user=self.user, operation=self.operation_1)
        delete_res = self.client.delete(f"{RECORD_URL}{record.id}/")
        self.assertEqual(delete_res.status_code, status.HTTP_204_NO_CONTENT)

        res = self.client.get(RECORD_URL)
        self.assertEqual(res.data["count"], 0)
