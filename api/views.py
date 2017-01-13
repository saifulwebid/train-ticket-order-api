from rest_framework import generics,viewsets,views, status
from .models import *
from .serializers import *
import datetime
from django.db import connection
from rest_framework.response import Response
from time import gmtime, strftime

class StasiunList(generics.ListCreateAPIView):
    queryset = Stasiun.objects.all()
    serializer_class = StasiunSerializer

class StasiunDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stasiun.objects.all()
    serializer_class = StasiunSerializer

class LayananKeretaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LayananKereta.objects.all()
    serializer_class = LayananKeretaSerializer

class RangkaianPerjalananList(generics.ListAPIView):
    serializer_class = RangkaianPerjalananSerializer

    def get_queryset(self):
        tahun = int(self.kwargs['tahun'])
        bulan = int(self.kwargs['bulan'])
        hari = int(self.kwargs['hari'])
        besok = hari + 1
        asal_id = self.kwargs['asal_id']
        tujuan_id = self.kwargs['tujuan_id']
        layanan = RangkaianPerjalanan.objects.raw("""SELECT *
                                         FROM rangkaian_perjalanan
                                         WHERE (
                                         jenis_perjalanan =  'B'
                                         AND id_stasiun =  %s
                                         AND waktu BETWEEN STR_TO_DATE(  '%s/%s/%s',  '%%Y/%%m/%%d' )
                                         AND STR_TO_DATE(  '%s/%s/%s',  '%%Y/%%m/%%d' )
                                         )
                                         OR (
                                         jenis_perjalanan =  'D'
                                         AND id_stasiun =  %s
                                         AND waktu BETWEEN STR_TO_DATE(  '%s/%s/%s',  '%%Y/%%m/%%d' )
                                         AND STR_TO_DATE(  '%s/%s/%s',  '%%Y/%%m/%%d' )
                                            )
                                         ORDER BY waktu
                                    """,
                                    [asal_id,tahun,bulan,hari,tahun,bulan,besok,tujuan_id,tahun,bulan,hari,tahun,bulan,besok])
        return layanan

class BookingDetail(generics.ListCreateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        kode_pembayaran = int(self.kwargs['pembayaran'])
        booking = Booking.objects.raw("""SELECT *
                                         FROM booking b, pembayaran p
                                         WHERE b.kode_booking = p.kode_booking AND p.kode_pembayaran = %s""",
                                         [kode_pembayaran])
        return booking

class BookingList(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class PemesanList(generics.ListCreateAPIView):
    queryset = Pemesan.objects.all()
    serializer_class = PemesanSerializer


class PenumpangList(generics.ListCreateAPIView):
    queryset = Penumpang.objects.all()
    serializer_class = PenumpangSerializer

class CaraBayarList(generics.ListCreateAPIView):
    queryset = CaraBayar.objects.all()
    serializer_class = CaraBayarSerializer

class PembayaranList(generics.ListCreateAPIView):
    queryset = Pembayaran.objects.all()
    serializer_class = PembayaranSerializer

class PembayaranDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pembayaran.objects.all()
    serializer_class = PembayaranSerializer
