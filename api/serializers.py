from rest_framework import serializers
from .models import *


class KeretaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kereta
        fields = '__all__'


class LayananKeretaSerializer(serializers.ModelSerializer):
    kereta = KeretaSerializer(read_only=True)
    id_kereta = serializers.PrimaryKeyRelatedField(
        queryset=Kereta.objects.all(), source='kereta')

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
        exclude = ('booking', )


class PenumpangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Penumpang
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    pemesan = PemesanSerializer(read_only=True)
    penumpang = PenumpangSerializer(many=True, read_only=True)
    layanan_kereta = LayananKeretaSerializer(read_only=True)
    id_layanan_kereta = serializers.PrimaryKeyRelatedField(
        queryset=LayananKereta.objects.all(), source='layanan_kereta')

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
