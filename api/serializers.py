from rest_framework import serializers
from .models import *

class KeretaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Kereta
		fields = '__all__'

class LayananKeretaSerializer(serializers.ModelSerializer):
	class Meta:
		model = LayananKereta
		fields = '__all__'

class TipePembayaranSerializer(serializers.ModelSerializer):
	class Meta:
		model = TipePembayaran
		fields = '__all__'

class PembayaranSerializer(serializers.ModelSerializer):
	class Meta:
		model = Pembayaran
		fields = '__all__'

class PemesanSerializer(serializers.ModelSerializer):
	class Meta:
		model = Pemesan
		fields = '__all__'

class PenumpangSerializer(serializers.ModelSerializer):
	class Meta:
		model = Penumpang
		fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = '__all__'
		depth = 1

class RangkaianPerjalananSerializer(serializers.ModelSerializer):
	class Meta:
		model = RangkaianPerjalanan
		fields = '__all__'

class StasiunSerializer(serializers.ModelSerializer):
	class Meta:
		model = Stasiun
		fields = '__all__'

