# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from templates.dashboard.Connect_DB import getCarOwner, getColumnChart_p1, getLevel1Attributes, getLevel2Attributes, getPurpose, people_get_pie, people_get_path
import json
from django import forms
from dashboard.models import User
from django.shortcuts import render,render_to_response
# from New_Website.settings import username, password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

class UserForm(forms.Form):
    username = forms.CharField(label='username', max_length=50)
    password = forms.CharField(label='password', widget=forms.PasswordInput())


def my_login(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render_to_response('dashboard/index.html', {'userform': userform})
            else:
                return HttpResponse('wrong username or password, please re-input')
    else:
        userform = UserForm()
        return render_to_response('dashboard/login.html',{'userform':userform})

# @login_required
# def my_logout(request):
#     request = render_to_response('dashboard/login.html')
#     #清除cookie里保存的username
#     logout(request)
#     return request


# index page
def index(request):
    return render(request, 'dashboard/index.html')
# car dashboard page
@login_required
def carOwnerChartPage(request):
    return render(request, 'dashboard/carEchartPage.html')
# people dashboard page
@login_required
def peopleChartPage(request):
    return render(request, 'dashboard/peopleEChartPage.html')

# get car page data
# @login_required
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
# @login_required
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


