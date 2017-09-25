from django.conf.urls import include, url
from django.contrib import admin
from .views import index

urlpatterns = [
    # index
    url(r'^$', index, name='index')
]
