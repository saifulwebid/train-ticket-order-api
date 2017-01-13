from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^stasiun/$', views.StasiunList.as_view()),
    url(r'^layanan/(?P<pk>[0-9]+)/$',views.LayananKeretaDetail.as_view()),
    url(r'^perjalanan/$', views.RangkaianPerjalananList.as_view()),
    url(r'^perjalanan/(?P<tahun>\d+)/(?P<bulan>\d+)/(?P<hari>\d+)/(?P<asal_id>.+)/(?P<tujuan_id>.+)/(?P<jml_penumpang>\d+)/$', views.RangkaianPerjalananList.as_view()),
    url(r'^pemesan/$',views.PemesanList.as_view()),
    url(r'^penumpang/$',views.PenumpangList.as_view()),
    url(r'^pembayaran/$',views.PembayaranList.as_view()),
    url(r'^pembayaran/(?P<pk>[0-9]+)/$',views.PembayaranDetail.as_view()),
    url(r'^carabayar/$',views.CaraBayarList.as_view()),
    url(r'^booking/(?P<pembayaran>\d+)/$',views.BookingDetail.as_view()),
    url(r'^booking/$',views.BookingList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
