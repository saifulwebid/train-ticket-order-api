from rest_framework import generics
from .models import *
from .serializers import *


class StasiunList(generics.ListCreateAPIView):
    queryset = Stasiun.objects.all()
    serializer_class = StasiunSerializer


class StasiunDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stasiun.objects.all()
    serializer_class = StasiunSerializer


class LayananKeretaList(generics.ListCreateAPIView):
    queryset = LayananKereta.objects.all()
    serializer_class = LayananKeretaSerializer


class LayananKeretaDetail(generics.RetrieveUpdateDestroyAPIView):
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
