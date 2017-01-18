from rest_framework import serializers
from .models import *
from django.core.exceptions import ObjectDoesNotExist


class KeretaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kereta
        fields = '__all__'


class LayananKeretaSerializer(serializers.ModelSerializer):
    kereta = KeretaSerializer()

    class Meta:
        model = LayananKereta
        exclude = ('kapasitas', )


class LayananKeretaLookupSerializer(serializers.ModelSerializer):
    kereta = KeretaSerializer()
    sisa_kursi = serializers.IntegerField()
    asal = serializers.SerializerMethodField()
    tujuan = serializers.SerializerMethodField()

    def get_asal(self, obj):
        stasiun = Stasiun.objects.get(id_stasiun=self.context['asal'])
        perjalanan_stasiun = obj.rangkaian_perjalanan.get(
            stasiun=stasiun, jenis_perjalanan="B")

        return {
            'stasiun': {
                'id_stasiun': stasiun.id_stasiun,
                'nama_stasiun': stasiun.nama_stasiun
            },
            'waktu': perjalanan_stasiun.waktu
        }

    def get_tujuan(self, obj):
        stasiun = Stasiun.objects.get(id_stasiun=self.context['tujuan'])
        perjalanan_stasiun = obj.rangkaian_perjalanan.get(
            stasiun=stasiun, jenis_perjalanan="D")

        return {
            'stasiun': {
                'id_stasiun': stasiun.id_stasiun,
                'nama_stasiun': stasiun.nama_stasiun
            },
            'waktu': perjalanan_stasiun.waktu
        }

    class Meta:
        model = LayananKereta
        fields = '__all__'


class CaraBayarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaraBayar
        fields = '__all__'


class WritePembayaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pembayaran
        exclude = ('booking', 'waktu_pembayaran', 'waktu_penagihan')


class BayarBookingSerializer(serializers.ModelSerializer):
    kode_pembayaran = serializers.IntegerField()

    def validate_kode_pembayaran(self, value):
        try:
            pembayaran = Pembayaran.objects.get(kode_pembayaran=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                "Kode pembayaran does not exists")

        if pembayaran.waktu_pembayaran is not None:
            raise serializers.ValidationError("Booking sudah dibayar")

        return value

    class Meta:
        model = Pembayaran
        fields = ('kode_pembayaran', )


class PembayaranSerializer(serializers.ModelSerializer):
    kode_booking = serializers.SerializerMethodField()
    batas_akhir_pembayaran = serializers.DateTimeField()

    def get_kode_booking(self, obj):
        if obj.waktu_pembayaran is None:
            return None

        return obj.booking.kode_booking

    class Meta:
        model = Pembayaran
        exclude = ('booking', )
        depth = 1


class PemesanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pemesan
        exclude = ('booking', )


class PenumpangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Penumpang
        exclude = ('id_penumpang', 'booking', )


class WriteBookingSerializer(serializers.ModelSerializer):
    jumlah_penumpang = serializers.IntegerField(min_value=1, max_value=4)

    class Meta:
        model = Booking
        exclude = ('waktu_mulai_booking', )


class BookingSerializer(serializers.ModelSerializer):
    kode_booking = serializers.SerializerMethodField()
    pemesan = PemesanSerializer(read_only=True)
    penumpang = PenumpangSerializer(many=True, read_only=True)
    pembayaran = PembayaranSerializer(read_only=True)
    layanan_kereta = LayananKeretaSerializer(read_only=True)
    valid = serializers.BooleanField()

    def get_kode_booking(self, obj):
        if 'cek-kode-booking' in self.context:
            if obj.pembayaran.waktu_pembayaran is None:
                return None

        return obj.kode_booking

    class Meta:
        model = Booking
        fields = '__all__'
        depth = 1


class StasiunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stasiun
        fields = '__all__'
