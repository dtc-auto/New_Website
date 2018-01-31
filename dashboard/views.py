# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
import csv
import urllib.request
import urllib.parse
import urllib
from templates.dashboard.Connect_DB \
    import getCarOwner, getColumnChart_p1, getLevel1Attributes, getLevel2Attributes, getPurpose, people_get_pie, people_get_path, CP_get_cluster, Config_get_config, Config_get_config_local, Config_get_company, Config_get_model
import json
from django import forms
from django.shortcuts import render,render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

class UserForm(forms.Form):
    username = forms.CharField(label='username', max_length=50)
    password = forms.CharField(label='password', widget=forms.PasswordInput())


def my_login(request):
    # next__ = request.get[next]
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
                    # return render_to_response(next__, {'userform': userform})
                else:
                    return HttpResponse('wrong username or password, please re-input')
            else:
                return HttpResponse('wrong username or password, please re-input')
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
@login_required
def LTPChartPage(request):
    return render(request, 'dashboard/LTP_Page.html')
@login_required
def CPChartPage(request):
    return render(request, 'dashboard/CP_Page.html')
@login_required
def ConfigChartPage(request):
    return render(request, 'dashboard/ConfigPage.html')

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

# get LTP
def LTPChart(request):
    text = request.GET.get('a', '')
    text = urllib.parse.quote(text.encode('utf8'))
    # 词性url
    url_pos = "https://api.ltp-cloud.com/analysis/?" \
          "api_key=C1H4c7k3j9LIApERArIRNF7ARHKRIPdqWI9xhMue&" \
          "text={0}" \
          "&pattern=pos" \
          "&format=plain".format(text)
    result_pos = urllib.request.urlopen(url_pos)  # POST method
    content_pos = result_pos.read().strip().decode('utf-8')
    content_pos_list = content_pos.split()
    return_text_pos = ''
    for i in range(0,len(content_pos_list)):
        if '__' in content_pos_list[i]:
            word = content_pos_list[i].replace("__", "_ _").replace(" _", "(")
        else:
            word = content_pos_list[i].replace("_", "(")
        word += ')  '
        return_text_pos += word

    # 分词url
    url_ws = "https://api.ltp-cloud.com/analysis/?" \
          "api_key=C1H4c7k3j9LIApERArIRNF7ARHKRIPdqWI9xhMue&" \
          "text={0}" \
          "&pattern=ws" \
          "&format=plain".format(text)
    result_ws = urllib.request.urlopen(url_ws)  # POST method
    content_ws = result_ws.read().strip().decode('utf-8').replace(" ", "    ")
    return_text_ws = content_ws
    r_dtc = {'pos': return_text_pos, 'ws': return_text_ws}
    return HttpResponse(json.dumps(r_dtc), content_type='application/json')

# get CP
# @login_required
def CPChart(request):
    # r_dtc = pd.read_csv('../dashboard/static/plot.csv', usecols=['value', 'slevel'], encoding="gb2312")
    data_cluster = CP_get_cluster()
    dict_ = {'cluster': data_cluster}
    return HttpResponse(json.dumps(dict_), content_type='application/json')



# get Config_company
# @login_required
def ConfigCompany(request):
    id_ = request.GET.get('id', '')
    dict_city =[{"companyId":188,"companyName":"D-大众(进口)","seriesList":[{"seriesId":110,"seriesName":"辉腾","seriesEnglish":"phaeton","seriesLetter":"H"},{"seriesId":111,"seriesName":"途锐","seriesEnglish":"touareg","seriesLetter":"T"},{"seriesId":115,"seriesName":"甲壳虫","seriesEnglish":"beetle","seriesLetter":"J"},{"seriesId":116,"seriesName":"大众Eos","seriesEnglish":"eos","seriesLetter":"D"},{"seriesId":1110,"seriesName":"尚酷","seriesEnglish":"scirocco","seriesLetter":"S"},{"seriesId":1621,"seriesName":"Tiguan(进口)","seriesEnglish":"tiguan","seriesLetter":"T"},{"seriesId":2327,"seriesName":"迈特威","seriesEnglish":"multivan","seriesLetter":"M"},{"seriesId":3704,"seriesName":"PASSAT 进口","seriesEnglish":"vw-passat","seriesLetter":"P"},{"seriesId":4304,"seriesName":"大众CC 进口","seriesEnglish":"vwcc-1","seriesLetter":"D"},{"seriesId":4305,"seriesName":"迈腾(进口)","seriesEnglish":"magotan-1","seriesLetter":"M"},{"seriesId":5325,"seriesName":"高尔夫(进口)","seriesEnglish":"golf-1","seriesLetter":"G"},{"seriesId":5326,"seriesName":"夏朗","seriesEnglish":"xailang","seriesLetter":"X"},{"seriesId":103800,"seriesName":"凯路威","seriesEnglish":"caravelle","seriesLetter":"K"},{"seriesId":107220,"seriesName":"蔚揽","seriesEnglish":"weilan","seriesLetter":"W"}]},{"companyId":187,"companyName":"S-上汽大众","seriesList":[{"seriesId":104,"seriesName":"桑塔纳","seriesEnglish":"santana","seriesLetter":"S"},{"seriesId":105,"seriesName":"桑塔纳志俊","seriesEnglish":"vista","seriesLetter":"S"},{"seriesId":112,"seriesName":"途安","seriesEnglish":"touran","seriesLetter":"T"},{"seriesId":113,"seriesName":"朗逸","seriesEnglish":"lavida","seriesLetter":"L"},{"seriesId":2359,"seriesName":"PASSAT新领驭","seriesEnglish":"newpassat","seriesLetter":"P"},{"seriesId":2824,"seriesName":"途观L","seriesEnglish":"csvw-tiguan","seriesLetter":"T"},{"seriesId":3244,"seriesName":"POLO","seriesEnglish":"polo","seriesLetter":"P"},{"seriesId":5344,"seriesName":"帕萨特","seriesEnglish":"passat-1","seriesLetter":"P"},{"seriesId":5345,"seriesName":"高尔","seriesEnglish":"gol-1","seriesLetter":"G"},{"seriesId":101626,"seriesName":"朗行","seriesEnglish":"granlavida","seriesLetter":"L"},{"seriesId":102402,"seriesName":"朗境","seriesEnglish":"crosslavida","seriesLetter":"L"},{"seriesId":102620,"seriesName":"桑塔纳经典","seriesEnglish":"santana-classical","seriesLetter":"S"},{"seriesId":104763,"seriesName":"凌渡","seriesEnglish":"lamando","seriesLetter":"L"},{"seriesId":106020,"seriesName":"桑塔纳·浩纳","seriesEnglish":"gransantana","seriesLetter":"S"},{"seriesId":107382,"seriesName":"辉昂","seriesEnglish":"phideon","seriesLetter":"H"},{"seriesId":108501,"seriesName":"途昂","seriesEnglish":"g-suv","seriesLetter":"T"},{"seriesId":109060,"seriesName":"途观","seriesEnglish":"tuguan","seriesLetter":"T"}]},{"companyId":186,"companyName":"Y-一汽-大众","seriesList":[{"seriesId":103,"seriesName":"捷达","seriesEnglish":"jetta","seriesLetter":"J"},{"seriesId":107,"seriesName":"高尔夫","seriesEnglish":"golf","seriesLetter":"G"},{"seriesId":108,"seriesName":"速腾","seriesEnglish":"sagitar","seriesLetter":"S"},{"seriesId":1109,"seriesName":"CC","seriesEnglish":"vwcc","seriesLetter":"C"},{"seriesId":2325,"seriesName":"宝来","seriesEnglish":"bora","seriesLetter":"B"},{"seriesId":2348,"seriesName":"宝来经典","seriesEnglish":"bora-tc","seriesLetter":"B"},{"seriesId":5310,"seriesName":"开迪","seriesEnglish":"kaidi-1","seriesLetter":"K"},{"seriesId":6708,"seriesName":"迈腾","seriesEnglish":"b7l","seriesLetter":"M"},{"seriesId":107580,"seriesName":"高尔夫 嘉旅","seriesEnglish":"gaoerfujialv","seriesLetter":"G"},{"seriesId":108120,"seriesName":"蔚领","seriesEnglish":"c-trek","seriesLetter":"W"}]}]
    # url_pos = "http://auto.chexun.com/public/companySeriesJsonForPara/load.do?id={0}".format(id_)
    # result_pos = urllib.request.urlopen(url_pos)  # POST method
    # content_pos = result_pos.read().strip().decode('utf-8')
    # content_pos = eval(content_pos)
    # return HttpResponse(json.dumps(content_pos))
    pos = Config_get_company(id_)
    return HttpResponse(json.dumps(pos))

# get Config_series
# @login_required
def ConfigSeriesChart(request):
    id_ = request.GET.get('id', '')
    # url_pos = "http://auto.chexun.com/public/yearModelJsonForPara/load.do?id={0}".format(id_)
    # result_pos = urllib.request.urlopen(url_pos)  # POST method
    # content_pos = result_pos.read().strip().decode('utf-8')
    # content_pos = eval(content_pos)
    content_pos = Config_get_model(id_)
    return HttpResponse(json.dumps(content_pos))

# get Config_modle
# @login_required
def ConfigModleChart(request):
    id_ = request.GET.get('modelId', '')
    content_pos = Config_get_config_local(id_)
    return HttpResponse(json.dumps(content_pos), content_type='application/json')