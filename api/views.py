from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


class StasiunList(generics.ListAPIView):
    queryset = Stasiun.objects.all()
    serializer_class = StasiunSerializer


class CaraBayarList(generics.ListAPIView):
    queryset = CaraBayar.objects.all()
    serializer_class = CaraBayarSerializer


class CaraBayarDariBooking(generics.GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == "GET":
            return CaraBayarSerializer

        return WritePembayaranSerializer

    def get(self, request, pk, *args, **kwargs):
        try:
            booking = Booking.objects.get(kode_booking=int(pk))
            queryset = Pembayaran.objects.get(booking=booking).cara_bayar
        except ObjectDoesNotExist:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND)

        print(repr(queryset))
        serializer = CaraBayarSerializer(queryset)
        return Response(serializer.data)

    def post(self, request, pk, *args, **kwargs):
        try:
            booking = Booking.objects.get(kode_booking=int(pk))
        except ObjectDoesNotExist:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND)

        if hasattr(booking, 'pembayaran'):
            return Response(
                {"detail": "Pembayaran already exists."},
                status=status.HTTP_409_CONFLICT)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                booking=booking,
                waktu_penagihan=timezone.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class PenumpangDetail(generics.ListCreateAPIView):
    kode_booking = None
    serializer_class = PenumpangSerializer

    def get_queryset(self):
        return Booking.objects.get(kode_booking=self.kode_booking).penumpang.all()

    def get(self, request, pk, *args, **kwargs):
        self.kode_booking = pk
        return self.list(request, *args, **kwargs)

    def create(self, request, pk, *args, **kwargs):
        self.kode_booking = pk
        booking = Booking.objects.get(kode_booking=pk)

        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        if serializer.is_valid():
            serializer.save(booking=booking)
            headers = self.get_success_headers(serializer.data)
            print(repr(headers))
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

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


class BayarBooking(generics.GenericAPIView):
    queryset = Pembayaran.objects.all()
    serializer_class = BayarBookingSerializer

    def post(self, request, *args, **kwargs):
        try:
            pembayaran = Pembayaran.objects.get(
                kode_pembayaran=request.data.get("kode_pembayaran"))
        except ObjectDoesNotExist:
            pembayaran = None

        serializer = BayarBookingSerializer(pembayaran, data=request.data)
        if serializer.is_valid():
            serializer.save(waktu_pembayaran=timezone.now())

            pembayaran = Pembayaran.objects.get(
                kode_pembayaran=request.data.get("kode_pembayaran"))
            response_serializer = PembayaranSerializer(pembayaran)
            return Response(response_serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
