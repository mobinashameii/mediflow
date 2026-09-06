from django.conf import settings
from django.db import models
from apps.clinics.models import Clinic
from django.core.exceptions import ValidationError


class Appointment(models.Model):

    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Scheduled"
        CONFIRMED = "CONFIRMED", "Confirmed"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"
        NO_SHOW = "NO_SHOW", "No Show"

    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.CASCADE,
        related_name="appointments",
    )

    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_appointments",
    )
    
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_appointments",
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError(
                "End time must be after start time."
            )

        if self.doctor.role != self.doctor.Role.DOCTOR:
            raise ValidationError(
                "Selected doctor must have DOCTOR role."
            )

        if self.patient.role != self.patient.Role.PATIENT:
            raise ValidationError(
                "Selected patient must have PATIENT role."
            )

        if not self.clinic.doctors.filter(pk=self.doctor.pk).exists():
            raise ValidationError(
                "This doctor does not belong to the selected clinic."
            )

        if not self.clinic.patients.filter(pk=self.patient.pk).exists():
            raise ValidationError(
                "This patient does not belong to the selected clinic."
            )

        overlapping = Appointment.objects.filter(
            doctor=self.doctor,
            date=self.date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError(
                "This doctor already has an appointment during this time."
            )