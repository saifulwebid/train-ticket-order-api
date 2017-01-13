from rest_framework import serializers
from .models import *
import datetime


class StasiunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stasiun
        fields = '__all__'

class KeretaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kereta
        fields = '__all__'

class LayananKeretaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayananKereta
        fields = '__all__'
        depth = 1


class PemesanSerializer(serializers.ModelSerializer):
    kode_booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())

    def validate_kode_booking(self,values):
        booking = Booking.objects.get(kode_booking = values.kode_booking)

        if((datetime.datetime.now() -booking.waktu_mulai_booking.replace(tzinfo=None)).total_seconds() > 600):
            raise serializers.ValidationError("Waktu pengisian sudah melebihi ketentuan")
        return values

    class Meta:
        model = Pemesan
        fields = '__all__'

class PenumpangSerializer(serializers.ModelSerializer):

    def validate_kode_booking(self,values):
        booking = Booking.objects.get(kode_booking = values.kode_booking)

        if((datetime.datetime.now() -booking.waktu_mulai_booking.replace(tzinfo=None)).total_seconds() > 600):
            raise serializers.ValidationError("Waktu pengisian sudah melebihi ketentuan")
        return values

    class Meta:
        model = Penumpang
        fields = '__all__'

class PembayaranSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pembayaran
        fields = '__all__'

class CaraBayarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaraBayar
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    penumpang = PenumpangSerializer(many = True,read_only = True, source='penumpang_set')
    pemesan = PemesanSerializer(many = True,read_only = True,source='pemesan_set')
    pembayaran = PembayaranSerializer(many = True,read_only = True,source='pembayaran_set')
    class Meta:
        model = Booking
        fields = '__all__'

class RangkaianPerjalananSerializer(serializers.ModelSerializer):

    class Meta:
        model = RangkaianPerjalanan
        fields = '__all__'
        depth = 3
