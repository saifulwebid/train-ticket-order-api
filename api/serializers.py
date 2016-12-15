from rest_framework import serializers
from .models import *


class KeretaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kereta
        fields = '__all__'


class LayananKeretaSerializer(serializers.ModelSerializer):
    kereta = KeretaSerializer()

    class Meta:
        model = LayananKereta
        fields = '__all__'


class CaraBayarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaraBayar
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
    pemesan = PemesanSerializer(read_only=True)
    penumpang = PenumpangSerializer(many=True, read_only=True)

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
