from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^stasiun/$', views.stasiun_list),
	url(r'^stasiun/(?P<pk>[A-Z]+)/$', views.stasiun_detail),
]
