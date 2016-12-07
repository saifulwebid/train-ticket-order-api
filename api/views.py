from django.shortcuts import render

# Create your views here.

from rest_framework import mixins, generics
from .models import *
from .serializers import *

class StasiunList(generics.GenericAPIView,
		mixins.ListModelMixin,
		mixins.CreateModelMixin):
	queryset = Stasiun.objects.all()
	serializer_class = StasiunSerializer

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

class StasiunDetail(generics.GenericAPIView,
		mixins.RetrieveModelMixin,
		mixins.UpdateModelMixin,
		mixins.DestroyModelMixin):
	queryset = Stasiun.objects.all()
	serializer_class = StasiunSerializer

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)
