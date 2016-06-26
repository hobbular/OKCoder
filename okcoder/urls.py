from django.conf.urls import url

from . import views

app_name = "okcoder"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^init/$', views.init, name='init'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<b>[0-2])/(?P<p1>[0-9A-Z]{6})/(?P<p2>[0-9A-Z]{6})/results/$', views.results, name='results'),
    url(r'^(?P<p1>[0-9A-Z]{6})/(?P<p2>[0-9A-Z]{6})/play/$', views.play, name='play'),
]
