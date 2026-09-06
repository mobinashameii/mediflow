from datetime import date, time

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.accounts.models import User
from apps.clinics.models import Clinic
from apps.appointments.models import Appointment


class AppointmentModelTest(TestCase):

    def setUp(self):
        self.doctor = User.objects.create_user(
            username="doctor1",
            password="testpass123",
            role=User.Role.DOCTOR,
        )

        self.patient = User.objects.create_user(
            username="patient1",
            password="testpass123",
            role=User.Role.PATIENT,
        )

        self.clinic = Clinic.objects.create(
            name="Test Clinic",
            owner=self.doctor,
        )

        self.clinic.doctors.add(self.doctor)
        self.clinic.patients.add(self.patient)

    def test_valid_appointment(self):
        appointment = Appointment(
            clinic=self.clinic,
            doctor=self.doctor,
            patient=self.patient,
            date=date(2026, 9, 10),
            start_time=time(10, 0),
            end_time=time(10, 30),
        )

        appointment.full_clean()

        self.assertIsNone(appointment.pk)

        appointment.save()

        self.assertIsNotNone(appointment.pk)


    def test_patient_cannot_be_doctor(self):
        appointment = Appointment(
        clinic=self.clinic,
        doctor=self.patient,
        patient=self.patient,
        date=date(2026, 9, 11),
        start_time=time(11, 0),
        end_time=time(11, 30),
    )

        with self.assertRaises(ValidationError):
           appointment.full_clean()    

    def test_doctor_cannot_be_patient(self):
        appointment = Appointment(
        clinic=self.clinic,
        doctor=self.doctor,
        patient=self.doctor,
        date=date(2026, 9, 12),
        start_time=time(11, 0),
        end_time=time(11, 30),
    )

        with self.assertRaises(ValidationError):
          appointment.full_clean()
    def test_doctor_must_belong_to_clinic(self):
        other_doctor = User.objects.create_user(
        username="doctor2",
        password="testpass123",
        role=User.Role.DOCTOR,
    )

        appointment = Appointment(
        clinic=self.clinic,
        doctor=other_doctor,
        patient=self.patient,
        date=date(2026, 9, 13),
        start_time=time(11, 0),
        end_time=time(11, 30),
    )

        with self.assertRaises(ValidationError):
           appointment.full_clean()
           
    def test_patient_must_belong_to_clinic(self):
        other_patient = User.objects.create_user(
        username="patient2",
        password="testpass123",
        role=User.Role.PATIENT,
    )

        appointment = Appointment(
        clinic=self.clinic,
        doctor=self.doctor,
        patient=other_patient,
        date=date(2026, 9, 14),
        start_time=time(11, 0),
        end_time=time(11, 30),
    )

        with self.assertRaises(ValidationError):
          appointment.full_clean()      

    def test_doctor_cannot_have_overlapping_appointments(self):
        first_appointment = Appointment.objects.create(
        clinic=self.clinic,
        doctor=self.doctor,
        patient=self.patient,
        date=date(2026, 9, 15),
        start_time=time(10, 0),
        end_time=time(10, 30),
    )

        overlapping_appointment = Appointment(
        clinic=self.clinic,
        doctor=self.doctor,
        patient=self.patient,
        date=date(2026, 9, 15),
        start_time=time(10, 15),
        end_time=time(10, 45),
    )

        with self.assertRaises(ValidationError):
          overlapping_appointment.full_clean()      

    def test_start_time_must_be_before_end_time(self):
        appointment = Appointment(
        clinic=self.clinic,
        doctor=self.doctor,
        patient=self.patient,
        date=date(2026, 9, 16),
        start_time=time(11, 30),
        end_time=time(11, 0),
    )

        with self.assertRaises(ValidationError):
           appointment.full_clean()      
    def test_back_to_back_appointments_are_allowed(self):
        first_appointment = Appointment.objects.create(
        clinic=self.clinic,
        doctor=self.doctor,
        patient=self.patient,
        date=date(2026, 9, 17),
        start_time=time(10, 0),
        end_time=time(10, 30),
    )

        second_appointment = Appointment(
        clinic=self.clinic,
        doctor=self.doctor,
        patient=self.patient,
        date=date(2026, 9, 17),
        start_time=time(10, 30),
        end_time=time(11, 0),
    )

        second_appointment.full_clean()
        second_appointment.save()

        self.assertIsNotNone(second_appointment.pk)       

    def test_appointment_inside_existing_appointment_is_rejected(self):
        Appointment.objects.create(
        clinic=self.clinic,
        doctor=self.doctor,
        patient=self.patient,
        date=date(2026, 9, 18),
        start_time=time(10, 0),
        end_time=time(11, 0),
    )

        overlapping_appointment = Appointment(
        clinic=self.clinic,
        doctor=self.doctor,
        patient=self.patient,
        date=date(2026, 9, 18),
        start_time=time(10, 15),
        end_time=time(10, 45),
    )

        with self.assertRaises(ValidationError):
           overlapping_appointment.full_clean()    
    def test_appointment_covering_existing_appointment_is_rejected(self):
        Appointment.objects.create(
        clinic=self.clinic,
        doctor=self.doctor,
        patient=self.patient,
        date=date(2026, 9, 19),
        start_time=time(10, 0),
        end_time=time(11, 0),
    )

        overlapping_appointment = Appointment(
        clinic=self.clinic,
        doctor=self.doctor,
        patient=self.patient,
        date=date(2026, 9, 19),
        start_time=time(9, 30),
        end_time=time(11, 30),
    )

        with self.assertRaises(ValidationError):
           overlapping_appointment.full_clean()

    def test_appointment_overlapping_from_start_is_rejected(self):
        Appointment.objects.create(
        clinic=self.clinic,
        doctor=self.doctor,
        patient=self.patient,
        date=date(2026, 9, 20),
        start_time=time(10, 0),
        end_time=time(11, 0),
    )

        overlapping_appointment = Appointment(
        clinic=self.clinic,
        doctor=self.doctor,
        patient=self.patient,
        date=date(2026, 9, 20),
        start_time=time(9, 30),
        end_time=time(10, 30),
    )

        with self.assertRaises(ValidationError):
          overlapping_appointment.full_clean()
    def test_same_time_on_different_dates_is_allowed(self):
        Appointment.objects.create(
        clinic=self.clinic,
        doctor=self.doctor,
        patient=self.patient,
        date=date(2026, 9, 21),
        start_time=time(10, 0),
        end_time=time(11, 0),
    )

        second_appointment = Appointment(
        clinic=self.clinic,
        doctor=self.doctor,
        patient=self.patient,
        date=date(2026, 9, 22),
        start_time=time(10, 0),
        end_time=time(11, 0),
    )

        second_appointment.full_clean()
        second_appointment.save()

        self.assertIsNotNone(second_appointment.pk)   