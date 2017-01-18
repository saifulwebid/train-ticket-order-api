from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from datetime import datetime
from django.utils import timezone


class StasiunList(generics.ListAPIView):
    queryset = Stasiun.objects.all()
    serializer_class = StasiunSerializer


class CaraBayarList(generics.ListAPIView):
    queryset = CaraBayar.objects.all()
    serializer_class = CaraBayarSerializer


class LayananKeretaDetail(generics.RetrieveAPIView):
    queryset = LayananKereta.objects.all()
    serializer_class = LayananKeretaSerializer


class BookingList(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = WriteBookingSerializer

    def perform_create(self, serializer):
        serializer.save(waktu_mulai_booking=timezone.now())


class BookingDetail(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class PemesanDetail(
        generics.RetrieveAPIView):
    queryset = Pemesan.objects.all()
    serializer_class = PemesanSerializer

    def post(self, request, pk, *args, **kwargs):
        booking = Booking.objects.get(kode_booking=pk)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(booking=booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CariLayananKereta(APIView):
    def get(self, request,
            tahun, bulan, tanggal, asal, tujuan, format=None):
        tahun = int(tahun)
        bulan = int(bulan)
        tanggal = int(tanggal)

        tz = timezone.get_current_timezone()
        tanggal_berangkat = datetime(tahun, bulan, tanggal, tzinfo=tz)
        tanggal_berangkat = tanggal_berangkat.astimezone(tz=timezone.utc)
        tanggal_berangkat = tanggal_berangkat.replace(tzinfo=None)

        queryset = LayananKereta.cari(tanggal_berangkat, asal, tujuan)
        serializer = LayananKeretaSerializer(queryset, many=True)
        return Response(serializer.data)
