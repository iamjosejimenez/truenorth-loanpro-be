from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user import views

app_name = "user"

router = DefaultRouter()
router.register("", views.BalanceViewSet)

urlpatterns = [
    path("", views.CreateUserView.as_view(), name="create"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path("balance/", include(router.urls)),
]
