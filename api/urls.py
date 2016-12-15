from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^stasiun/$', views.StasiunList.as_view()),
    url(r'^stasiun/(?P<pk>[A-Z]+)/$', views.StasiunDetail.as_view()),
    url(r'^booking/$', views.BookingList.as_view()),
    url(r'^booking/(?P<pk>[0-9]+)/$', views.BookingDetail.as_view()),
    url(r'^layanan/$', views.LayananKeretaList.as_view()),
    url(r'^layanan/(?P<pk>[0-9]+)/$',
        views.LayananKeretaDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
