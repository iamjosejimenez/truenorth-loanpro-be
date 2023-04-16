from django.urls import include, path
from rest_framework.routers import DefaultRouter

from record import views

router = DefaultRouter()
router.register("", views.RecordViewSet)

app_name = "record"

urlpatterns = [
    path("", include(router.urls)),
]
