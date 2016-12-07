# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Booking(models.Model):
    kode_booking = models.IntegerField(primary_key=True)
    layanan_kereta = models.ForeignKey('LayananKereta', models.DO_NOTHING, db_column='id_layanan_kereta')
    jumlah_penumpang = models.IntegerField()
    waktu_mulai_booking = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'booking'


class Kereta(models.Model):
    id_kereta = models.IntegerField(primary_key=True)
    nama_kereta = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'kereta'


class LayananKereta(models.Model):
    id_layanan_kereta = models.IntegerField(primary_key=True)
    kereta = models.ForeignKey(Kereta, models.DO_NOTHING, db_column='id_kereta')
    kapasitas = models.IntegerField()
    harga_tiket = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'layanan_kereta'


class Pembayaran(models.Model):
    kode_pembayaran = models.IntegerField(primary_key=True)
    booking = models.ForeignKey(Booking, models.DO_NOTHING, db_column='kode_booking')
    tipe_pembayaran = models.ForeignKey('TipePembayaran', models.DO_NOTHING, db_column='id_tipe_pembayaran')
    waktu_penagihan = models.DateTimeField()
    waktu_pembayaran = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pembayaran'


class Pemesan(models.Model):
    booking = models.OneToOneField(Booking, models.DO_NOTHING, db_column='kode_booking', primary_key=True)
    nama_pemesan = models.CharField(max_length=64)
    email_pemesan = models.CharField(max_length=64)
    nomor_telepon_pemesan = models.CharField(max_length=16)
    alamat_pemesan = models.TextField()

    class Meta:
        managed = False
        db_table = 'pemesan'


class Penumpang(models.Model):
    id_penumpang = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, models.DO_NOTHING, db_column='kode_booking')
    nomor_identitas = models.CharField(max_length=24)
    nama_penumpang = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'penumpang'
        unique_together = (('booking', 'nomor_identitas'),)


class RangkaianPerjalanan(models.Model):
    id_rangkaian_perjalanan = models.AutoField(primary_key=True)
    layanan_kereta = models.ForeignKey(LayananKereta, models.DO_NOTHING, db_column='id_layanan_kereta')
    stasiun_kedatangan = models.ForeignKey('Stasiun', models.DO_NOTHING, db_column='stasiun_kedatangan', related_name='rangkaian_datang')
    stasiun_keberangkatan = models.ForeignKey('Stasiun', models.DO_NOTHING, db_column='stasiun_keberangkatan', related_name='rangkaian_berangkat')
    waktu_keberangkatan = models.DateTimeField()
    waktu_kedatangan = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'rangkaian_perjalanan'
        unique_together = (('layanan_kereta', 'stasiun_kedatangan', 'stasiun_keberangkatan'),)


class Stasiun(models.Model):
    id_stasiun = models.CharField(primary_key=True, max_length=3)
    nama_stasiun = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'stasiun'


class TipePembayaran(models.Model):
    id_tipe_pembayaran = models.IntegerField(primary_key=True)
    nama_tipe_pembayaran = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'tipe_pembayaran'
