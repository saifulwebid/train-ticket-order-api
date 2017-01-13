from rest_framework import generics
from .models import *
from .serializers import *


class StasiunList(generics.ListAPIView):
    queryset = Stasiun.objects.all()
    serializer_class = StasiunSerializer


class StasiunDetail(generics.RetrieveAPIView):
    queryset = Stasiun.objects.all()
    serializer_class = StasiunSerializer


class LayananKeretaList(generics.ListAPIView):
    queryset = LayananKereta.objects.all()
    serializer_class = LayananKeretaSerializer


class LayananKeretaDetail(generics.RetrieveAPIView):
    queryset = LayananKereta.objects.all()
    serializer_class = LayananKeretaSerializer


class BookingList(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class PemesanDetail(
        generics.RetrieveUpdateAPIView, generics.CreateAPIView):
    queryset = Pemesan.objects.all()
    serializer_class = PemesanSerializer
