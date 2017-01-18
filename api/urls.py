from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^stasiun/$', views.StasiunList.as_view()),
    url(r'^carabayar/$', views.CaraBayarList.as_view()),
    url(r'^booking/$', views.BookingList.as_view()),
    url(r'^booking/(?P<pk>[0-9]+)/$', views.BookingDetail.as_view()),
    url(r'^booking/(?P<pk>[0-9]+)/pemesan/$', views.PemesanDetail.as_view()),
    url(r'^booking/(?P<pk>[0-9]+)/penumpang/$', views.PenumpangDetail.as_view()),
    url(r'^booking/(?P<pk>[0-9]+)/carabayar/$', views.CaraBayarDariBooking.as_view()),
    url(r'^layanan/(?P<pk>[0-9]+)/$',
        views.LayananKeretaDetail.as_view()),
    url(r'^layanan/(?P<tahun>\d+)/(?P<bulan>\d+)/(?P<tanggal>\d+)/(?P<asal>.+)/(?P<tujuan>.+)/$',
        views.CariLayananKereta.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
