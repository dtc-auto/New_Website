from django.conf.urls import *
from . import views
from dashboard.views import carOwnerChartPage, carOwnerChart, peopleChartPage, peopleChart, my_login, LTPChartPage, LTPChart
urlpatterns = [
    # index
    url(r'^$', views.index, name='index'),
    # login
    url(r'^login', my_login, name='my_login'),
    # logout
    # url(r'^logout', my_logout, name='my_logout'),

    # car dashboard page
    url(r'^auto_page', carOwnerChartPage, name='carEchart'),
    url(r'^auto/$', carOwnerChart, name='carEchartPage'),
    # people dashboard page
    url(r'^people_page', peopleChartPage, name='peopleEchart'),
    url(r'^people/$', peopleChart, name='peopleEchartPage'),
    # LTP dashborad page
    url(r'^LTP_page', LTPChartPage, name='LTPChart'),
    url(r'^LTP/$', LTPChart, name='LTPPage'),
]


