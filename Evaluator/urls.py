from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', login, {'template_name': 'logout.html'}),
    url(r'^profile/$', views.profile, name='profile'),
    ]