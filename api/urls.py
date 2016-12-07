from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
	url(r'^stasiun/$', views.stasiun_list),
	url(r'^stasiun/(?P<pk>[A-Z]+)/$', views.stasiun_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
