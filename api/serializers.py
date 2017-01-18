from rest_framework import serializers
from .models import *
from django.utils import timezone


class KeretaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kereta
        fields = '__all__'


class RangkaianPerjalananSerializer(serializers.ModelSerializer):
    class Meta:
        model = RangkaianPerjalanan
        fields = '__all__'


class LayananKeretaSerializer(serializers.ModelSerializer):
    kereta = KeretaSerializer()
    rangkaian_perjalanan = RangkaianPerjalanan()
    sisa_kursi = serializers.IntegerField()

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


class WritePemesanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pemesan
        fields = '__all__'


class PenumpangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Penumpang
        fields = '__all__'


class WriteBookingSerializer(serializers.ModelSerializer):
    jumlah_penumpang = serializers.IntegerField(min_value=1, max_value=4)

    class Meta:
        model = Booking
        exclude = ('waktu_mulai_booking', )


class BookingSerializer(serializers.ModelSerializer):
    pemesan = PemesanSerializer(read_only=True)
    penumpang = PenumpangSerializer(many=True, read_only=True)
    pembayaran = PembayaranSerializer(read_only=True)
    layanan_kereta = LayananKeretaSerializer(read_only=True)
    valid_status = serializers.BooleanField()

    class Meta:
        model = Booking
        fields = '__all__'
        depth = 1


class StasiunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stasiun
        fields = '__all__'
