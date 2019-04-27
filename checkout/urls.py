from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^getDPScan/', views.getDPScan, name='getDPScan'),
    url(r'^routingTools/', views.routingTools, name='test-tool'),
]
