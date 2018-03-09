from django.conf.urls import *
from . import views
from django.conf.urls.static import static
from dashboard.views import carOwnerChartPage, carOwnerChart, peopleChartPage, peopleChart, my_login, LTPChartPage, LTPChart, \
    CPChartPage, CPChart, ConfigChartPage, ConfigCompany, ConfigSeriesChart, ConfigModleChart, priceChartPage, PriceModleChart, \
    PriceCompany, PriceSeries
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
    # CP dashboard page
    url(r'^CP_page', CPChartPage, name='CPChart'),
    url(r'^CP/$', CPChart, name='CPEchartPage'),
    # Config dashboard page
    url(r'^Config_page', ConfigChartPage, name='ConfigChart'),
    url(r'^Config/$', ConfigCompany, name='ConfigCompanyPage'),
    url(r'^Config_/$', ConfigSeriesChart, name='ConfigSeriesPage'),
    url(r'^Confi/$', ConfigModleChart, name='ConfigModlePage'),
    # price dashboard page
    url(r'^price_page', priceChartPage, name="pricePage"),
    url(r'^price_company/$', PriceCompany, name='PriceCompanyPage'),
    url(r'^price_series/$', PriceSeries, name='PriceSeriesPage'),
    url(r'^price/$', PriceModleChart, name="Price_ModlePage"),

]


