from django.conf.urls import url

from . import views

app_name = "okcoder"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^init/$', views.init, name='init'),
    url(r'^create/$', views.create, name='create'),
    url(r'^log/$', views.log, name='log'),
    url(r'^(?P<b>[0-2])/(?P<ps>[0-9A-Z]{6})/results/$', views.results, name='results'),
    url(r'^(?P<ps>[0-9A-Z]{6})/play/$', views.play, name='play'),
    url(r'^(?P<ps>[0-9A-Z]{6})/eval/$', views.eval, name='eval'),
    url(r'^(?P<ps>[0-9A-Z]{6})/evaluate/$', views.evaluate, name='evaluate'),
    url(r'^(?P<ps>[0-9A-Z]{6})/complete/$', views.complete, name='complete')
]
