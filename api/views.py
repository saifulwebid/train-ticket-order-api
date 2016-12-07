from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import *
from .serializers import *

class StasiunList(generics.ListCreateAPIView):
	queryset = Stasiun.objects.all()
	serializer_class = StasiunSerializer

class StasiunDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Stasiun.objects.all()
	serializer_class = StasiunSerializer

class BookingList(generics.ListCreateAPIView):
	queryset = Booking.objects.all()
	serializer_class = BookingSerializer

class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Booking.objects.all()
	serializer_class = BookingSerializer
