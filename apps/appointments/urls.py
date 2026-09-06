from django.urls import path

from .views import AppointmentCreateView, AppointmentDetailView


urlpatterns = [
    path(
        "appointments/",
        AppointmentCreateView.as_view(),
        name="appointment-create",
    ),
     path(
        "appointments/<int:pk>/",
        AppointmentDetailView.as_view(),
        name="appointment-detail",
    ),
]