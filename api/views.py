from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

@api_view(['GET', 'POST'])
def stasiun_list(request, format=None):
	if request.method == 'GET':
		stasiun = Stasiun.objects.all()
		serializer = StasiunSerializer(stasiun, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = StasiunSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def stasiun_detail(request, pk, format=None):
	try:
		stasiun = Stasiun.objects.get(pk=pk)
	except Stasiun.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = StasiunSerializer(stasiun)
		return Response(serializer.data)

	elif request.method == 'PUT':
		serializer = StasiunSerializer(stasiun, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
