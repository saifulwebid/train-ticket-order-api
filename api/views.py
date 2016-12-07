from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.http import Http404

class StasiunList(APIView):
	def get(self, request, format=None):
		stasiun = Stasiun.objects.all()
		serializer = StasiunSerializer(stasiun, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = StasiunSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StasiunDetail(APIView):
	def get_object(self, pk):
		try:
			return Stasiun.objects.get(pk=pk)
		except Stasiun.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		stasiun = self.get_object(pk)
		serializer = StasiunSerializer(stasiun)
		return Response(serializer.data)

	def post(self, request, pk, format=None):
		stasiun = self.get_object(pk)
		serializer = StasiunSerializer(stasiun, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		stasiun = self.get_object(pk)
		stasiun.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
