from django.conf.urls import url
from . import views
from dashboard.views import carOwnerChartPage, carOwnerChart, peopleChartPage, peopleChart, login
urlpatterns = [
    # index
    url(r'^$', views.index, name='index'),
    # car dashboard page
    url(r'^auto_page', carOwnerChartPage, name='carEchart'),
    url(r'^auto/$', carOwnerChart, name='carEchartPage'),
    # people dashboard page
    url(r'^people_page', peopleChartPage, name='peopleEchart'),
    url(r'^people/$', peopleChart, name='peopleEchartPage'),
    # login
    url(r'^login', login, name='login'),

]
