# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, render_to_response
from templates.dashboard.Connect_DB import getCarOwner, getColumnChart_p1, getLevel1Attributes, getLevel2Attributes, getPurpose, people_get_pie, people_get_path
import json
from django import forms
from django.shortcuts import render,render_to_response
from New_Website.settings import username, password

class UserForm(forms.Form):
    username = forms.CharField(label='username', max_length=50)
    password = forms.CharField(label='password', widget=forms.PasswordInput())


def login(request):
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            # 获取表单用户密码
            username_ = uf.cleaned_data['username']
            password_ = uf.cleaned_data['password']
            # 获取的表单数据与数据库进行比较

            if username == username_ and password == password_:
                return render_to_response('dashboard/carEchartPage.html')
            else:
                return HttpResponse("用户名或密码错误,请重新输入")
    else:
        uf = UserForm()
    return render_to_response("dashboard/login.html",{'uf':uf})



# index page
def index(request):
    return render(request, 'dashboard/index.html')
# car dashboard page
def carOwnerChartPage(request):
    return render(request, 'dashboard/carEchartPage.html')
# people dashboard page
def peopleChartPage(request):
    return render(request, 'dashboard/peopleEChartPage.html')

# get car page data
def carOwnerChart(request):
    # page 对应原页面 page 1-4
    target = request.GET.get('a', '')

    # 当 select 所有车型的时候进入 page_2_lv1
    if len(target) == 32:
        page_2_lv1 = getLevel1Attributes(target)
        dict = {'page_2_lv1': page_2_lv1}
        return HttpResponse(json.dumps(dict), content_type='application/json')

    # 当 select 包括维度时进入 page_2_lv2
    if len(target) >= 6:
        page_2_lv2 = getLevel2Attributes(target)
        dict = {'page_2_lv2': page_2_lv2}
        return HttpResponse(json.dumps(dict), content_type='application/json')

    # 当 select 单个车型时进入 page_1_map / page_1_stacked / page_2_lv1 / page_4_purpose
    page_1_map, map_max_data = getCarOwner(target)
    page_1_stacked = getColumnChart_p1()
    page_2_lv1 = getLevel1Attributes(target)
    page_4_purpose = getPurpose(target)
    dict = {'page_1_map': page_1_map,
            'page_1_map_max_data': map_max_data,
            'page_1_stacked': page_1_stacked,
            'page_2_lv1': page_2_lv1,
            'page_4_purpose': page_4_purpose}
    return HttpResponse(json.dumps(dict), content_type='application/json')
# get people page data
def peopleChart(request):
    target = request.GET.get('a', '')
    path = request.GET.get('path', '')

    # 当 select path 时进入 people_get_path
    if len(path) > 0:
        path = people_get_path(path)
        dict = {'path': path}
        return HttpResponse(json.dumps(dict), content_type='application/json')

    pie_data = people_get_pie(target)
    dict = {'people_get_pie': pie_data,
            }
    return HttpResponse(json.dumps(dict), content_type='application/json')


