from django.conf import settings
from django.db import models


class Clinic(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_clinics",
    )

    doctors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="doctor_clinics",
        blank=True,
    )

    patients = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="patient_clinics",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name