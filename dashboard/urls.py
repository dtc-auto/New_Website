from django.conf.urls import url
from . import views

urlpatterns = [
    # index
    url(r'^$', views.index, name='index'),
    # car dashboard page
    url(r'^auto_page', 'dashboard.views.carOwnerChartPage', name='carEchart'),
    url(r'^auto/$', 'dashboard.views.carOwnerChart', name='carEchartPage'),
    # people dashboard page
    url(r'^people_page', 'dashboard.views.peopleChartPage', name='carEchart'),
    url(r'^people/$', 'dashboard.views.peopleChart', name='carEchartPage'),

]
