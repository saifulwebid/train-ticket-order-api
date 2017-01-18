from __future__ import unicode_literals
from django.db import models
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta


class Booking(models.Model):
    kode_booking = models.AutoField(primary_key=True)
    layanan_kereta = models.ForeignKey(
        'LayananKereta', models.DO_NOTHING, db_column='id_layanan_kereta')
    jumlah_penumpang = models.IntegerField()
    waktu_mulai_booking = models.DateTimeField()

    def __get_valid(self):
        waktu_sekarang = timezone.now()
        waktu_booking = self.waktu_mulai_booking
        delta = waktu_sekarang - waktu_booking

        if self.penumpang.count() != self.jumlah_penumpang:
            # Proses input penumpang belum selesai
            return delta.total_seconds() <= 600  # 10 menit

        # Cek status pembayaran
        if hasattr(self, 'pembayaran'):
            if self.pembayaran.waktu_pembayaran is None:
                # Belum dibayar; jangka waktu pembayaran 2 jam
                delta = waktu_sekarang - self.pembayaran.waktu_penagihan
                return delta.total_seconds() <= 7200  # 2 jam

        # Sudah dibayar
        return True

    valid = property(__get_valid)

    class Meta:
        managed = False
        db_table = 'booking'


class CaraBayar(models.Model):
    id_cara_bayar = models.AutoField(primary_key=True)
    nama_cara_bayar = models.CharField(max_length=40)
    detil_cara_bayar = models.TextField()

    class Meta:
        managed = False
        db_table = 'cara_bayar'


class Kereta(models.Model):
    id_kereta = models.AutoField(primary_key=True)
    nama_kereta = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'kereta'


class LayananKereta(models.Model):
    id_layanan_kereta = models.AutoField(primary_key=True)
    kereta = models.ForeignKey(
        Kereta, models.DO_NOTHING, db_column='id_kereta')
    kapasitas = models.IntegerField()
    harga_tiket = models.IntegerField()

    def __hitung_sisa_kursi(self):
        durasi_pengisian = timezone.now() - timedelta(minutes=10)
        durasi_pembayaran = timezone.now() - timedelta(hours=2)
        count = self.booking_set.filter(
            Q(waktu_mulai_booking__gte=durasi_pengisian) |
            Q(pembayaran__waktu_penagihan__gte=durasi_pembayaran) |
            Q(pembayaran__waktu_pembayaran__isnull=False))
        count = count.aggregate(Sum('jumlah_penumpang'))

        if count["jumlah_penumpang__sum"] is None:
            count["jumlah_penumpang__sum"] = 0

        return self.kapasitas - count["jumlah_penumpang__sum"]

    sisa_kursi = property(__hitung_sisa_kursi)

    def cari(tanggal_berangkat, asal, tujuan):
        range_akhir = tanggal_berangkat + timedelta(days=1)
        args = [tanggal_berangkat, range_akhir, asal, tujuan]
        queryset = LayananKereta.objects.raw(
            '''SELECT lk.* FROM layanan_kereta lk, rangkaian_perjalanan asal,
            rangkaian_perjalanan tujuan
                WHERE lk.id_layanan_kereta = asal.id_layanan_kereta
                    AND asal.id_layanan_kereta = tujuan.id_layanan_kereta
                    AND asal.jenis_perjalanan = "B"
                    AND tujuan.jenis_perjalanan = "D"
                    AND asal.waktu < tujuan.waktu
                    AND asal.waktu
                        BETWEEN %s AND %s
                    AND asal.id_stasiun = %s
                    AND tujuan.id_stasiun = %s''', args)
        return queryset

    class Meta:
        managed = False
        db_table = 'layanan_kereta'


class Pembayaran(models.Model):
    kode_pembayaran = models.AutoField(primary_key=True)
    booking = models.OneToOneField(
        Booking, models.DO_NOTHING, db_column='kode_booking')
    cara_bayar = models.ForeignKey(
        CaraBayar, models.DO_NOTHING, db_column='id_cara_bayar')
    waktu_penagihan = models.DateTimeField()
    waktu_pembayaran = models.DateTimeField(blank=True, null=True)

    def __get_batas_akhir_pembayaran(self):
        return self.waktu_penagihan + timedelta(seconds=60 * 60 * 2)

    batas_akhir_pembayaran = property(__get_batas_akhir_pembayaran)

    class Meta:
        managed = False
        db_table = 'pembayaran'


class Pemesan(models.Model):
    booking = models.OneToOneField(
        Booking, models.DO_NOTHING, db_column='kode_booking', primary_key=True)
    nama_pemesan = models.CharField(max_length=64)
    email_pemesan = models.CharField(max_length=64)
    nomor_telepon_pemesan = models.CharField(max_length=16)
    alamat_pemesan = models.TextField()

    class Meta:
        managed = False
        db_table = 'pemesan'


class Penumpang(models.Model):
    id_penumpang = models.AutoField(primary_key=True)
    booking = models.ForeignKey(
        Booking, models.DO_NOTHING, db_column='kode_booking',
        related_name='penumpang')
    nomor_identitas = models.CharField(max_length=24)
    nama_penumpang = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'penumpang'
        unique_together = (('booking', 'nomor_identitas'),)


class RangkaianPerjalanan(models.Model):
    id_rangkaian_perjalanan = models.AutoField(primary_key=True)
    layanan_kereta = models.ForeignKey(
        LayananKereta, models.DO_NOTHING, db_column='id_layanan_kereta',
        related_name='rangkaian_perjalanan')
    stasiun = models.ForeignKey(
        'Stasiun', models.DO_NOTHING, db_column='id_stasiun')
    jenis_perjalanan = models.CharField(max_length=1)
    waktu = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'rangkaian_perjalanan'
        unique_together = (
            ('layanan_kereta', 'stasiun', 'jenis_perjalanan'),)


class Stasiun(models.Model):
    id_stasiun = models.CharField(primary_key=True, max_length=3)
    nama_stasiun = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'stasiun'
