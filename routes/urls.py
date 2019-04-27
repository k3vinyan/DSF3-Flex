from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^deleteRoute$', views.deleteRoute, name='deleteRoute'),
    url(r'^addRoute$', views.addRoute, name='addRoute'),
]