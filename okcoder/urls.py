from django.conf.urls import url

from . import views

app_name = "okcoder"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^init/$', views.init, name='init'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<b>[0-2])/results/$', views.results, name='results'),
]
