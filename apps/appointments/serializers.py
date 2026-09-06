from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.appointments.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "id",
            "clinic",
            "doctor",
            "patient",
            "date",
            "start_time",
            "end_time",
            "status",
            "notes",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        if self.instance:
          appointment = self.instance

          for attr, value in attrs.items():
            setattr(appointment, attr, value)
        else:
          appointment = Appointment(**attrs)

        try:
          appointment.full_clean()
        except DjangoValidationError as exc:
          raise serializers.ValidationError(exc.message_dict)

        return attrs