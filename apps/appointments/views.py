from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentCreateView(APIView):

    def get(self, request):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)

        if serializer.is_valid():
            appointment = serializer.save()

            return Response(
                AppointmentSerializer(appointment).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class AppointmentDetailView(APIView):

    def get(self, request, pk):
        appointment = get_object_or_404(
            Appointment,
            pk=pk,
        )

        serializer = AppointmentSerializer(appointment)

        return Response(serializer.data)

    def patch(self, request, pk):
        appointment = get_object_or_404(
            Appointment,
            pk=pk,
        )

        serializer = AppointmentSerializer(
            appointment,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            appointment = serializer.save()

            return Response(
                AppointmentSerializer(appointment).data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request, pk):
        appointment = get_object_or_404(
            Appointment,
            pk=pk,
        )

        serializer = AppointmentSerializer(
            appointment,
            data=request.data,
        )

        if serializer.is_valid():
            appointment = serializer.save()

            return Response(
                AppointmentSerializer(appointment).data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
