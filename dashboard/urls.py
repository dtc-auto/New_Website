from django.conf.urls import url
from . import views

urlpatterns = [
    # index
    url(r'^$', views.index, name='index'),
    # dashboard page
    url(r'^dashboard', 'dashboard.views.carOwnerChartPage', name='carEchart'),
    url(r'^dash/$', 'dashboard.views.carOwnerChart', name='carEchartPage'),

]
