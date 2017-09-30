# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from templates.dashboard.Connect_DB import getCarOwner, getColumnChart_p1, getLevel1Attributes, getLevel2Attributes, getPurpose
import json
# Create your views here.
# index page
def index(request):
    return render(request, 'dashboard/index.html')
# dashboard page
def carOwnerChartPage(request):
    return render(request, 'dashboard/carEchartPage.html')

def carOwnerChart(request):
    target = request.GET.get('a', '')
    list1 = getCarOwner(target)
    list2 = getColumnChart_p1()
    list3 = getPurpose(target)
    dict = {'list1': list1, 'list2': list2, 'list3': list3}
    return HttpResponse(json.dumps(dict), content_type='application/json')
