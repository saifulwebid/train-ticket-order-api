from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *

class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

def stasiun_list(request):
	if request.method == 'GET':
		stasiun = Stasiun.objects.all()
		serializer = StasiunSerializer(stasiun, many=True)
		return JSONResponse(serializer.data)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = StasiunSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)

def stasiun_detail(request, pk):
	try:
		stasiun = Stasiun.objects.get(pk=pk)
	except Stasiun.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = StasiunSerializer(stasiun)
		return JSONResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = StasiunSerializer(stasiun, data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		snippet.delete()
		return HttpResponse(status=204)
