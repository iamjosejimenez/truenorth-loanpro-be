from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user import views

app_name = "user"

router = DefaultRouter()
router.register("balances", views.BalanceViewSet, basename="balances")

urlpatterns = [
    path("", views.CreateUserView.as_view(), name="create"),
    path("", include((router.urls, "balances"), namespace="balances"), name="balance"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
]
