from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
<<<<<<< HEAD
    url(r'^drivers/', views.seedDrivers, name='seedDrivers'),
    url(r'^routes/', views.seedRoutes, name='addRoutes'),
=======
    url(r'^seeddrivers/', views.seedDrivers, name='seedDrivers'),
    url(r'^seedroutes/', views.seedRoutes, name='addRoutes'),
>>>>>>> development
]
