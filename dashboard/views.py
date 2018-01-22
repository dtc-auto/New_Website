# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
import csv
import urllib.request
import urllib.parse
import urllib
from templates.dashboard.Connect_DB \
    import getCarOwner, getColumnChart_p1, getLevel1Attributes, getLevel2Attributes, getPurpose, people_get_pie, people_get_path, CP_get_cluster, Config_get_config
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
    url_pos = "http://auto.chexun.com/public/companySeriesJsonForPara/load.do?id={0}".format(id_)
    result_pos = urllib.request.urlopen(url_pos)  # POST method
    content_pos = result_pos.read().strip().decode('utf-8')
    content_pos = eval(content_pos)
    return HttpResponse(json.dumps(content_pos))

# get Config_series
# @login_required
def ConfigSeriesChart(request):
    id_ = request.GET.get('id', '')
    url_pos = "http://auto.chexun.com/public/yearModelJsonForPara/load.do?id={0}".format(id_)
    result_pos = urllib.request.urlopen(url_pos)  # POST method
    content_pos = result_pos.read().strip().decode('utf-8')
    content_pos = eval(content_pos)
    return HttpResponse(json.dumps(content_pos))

# get Config_modle
# @login_required
def ConfigModleChart(request):
    id_ = request.GET.get('modelId', '')
    content_pos = Config_get_config(id_)
    # content_pos = '{"returncode":0,"message":"成功","result":{"paramtypeitems":[{"typeId":1,"name":"基础参数","paramitems":[{"name":"车型名称","id":0,"valueitems":[{"specid":5152,"value":"辉腾 2011款 6.0L W12 4座加长Individual版"}]},{"name":"年代款","id":0,"valueitems":[{"specid":5152,"value":2011}]},{"name":"厂商指导价","id":0,"valueitems":[{"specid":5152,"value":"241.2万元"}]},{"name":"全国经销商最低价","id":0,"valueitems":[{"specid":5152,"value":"241.2-241.2万元"}]},{"name":"实测100-0制动（m）","id":3,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"官方0-100加速（s）","id":2,"valueitems":[{"specid":5152,"value":"6.1"}]},{"name":"实测油耗（L）","id":4,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"最高车速（km/h）","id":1,"valueitems":[{"specid":5152,"value":"250.0"}]},{"name":"工信部综合油耗（L）","id":5,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"排量(L)","id":22,"valueitems":[{"specid":5152,"value":"6.0"}]},{"name":"长*宽*高(mm)","id":7,"valueitems":[{"specid":5152,"value":"5175*1903*1450"}]},{"name":"整车质保","id":6,"valueitems":[{"specid":5152,"value":"两年不限公里"}]},{"name":"车身结构","id":15,"valueitems":[{"specid":5152,"value":"三厢车"}]},{"name":"挡位个数","id":43,"valueitems":[{"specid":5152,"value":"5"}]},{"name":"变速箱类型","id":44,"valueitems":[{"specid":5152,"value":"自动变速箱(AT)"}]}]},{"typeId":2,"name":"车身参数","paramitems":[{"name":"轴距(mm)","id":10,"valueitems":[{"specid":5152,"value":"3001"}]},{"name":"前轮距(mm)","id":11,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"后轮距(mm)","id":12,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"最小离地间隙(mm)","id":13,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"整备质量(Kg)","id":14,"valueitems":[{"specid":5152,"value":"2383"}]},{"name":"车门数(个)","id":16,"valueitems":[{"specid":5152,"value":"4"}]},{"name":"座位数(个)","id":17,"valueitems":[{"specid":5152,"value":"4"}]},{"name":"油箱容积(L)","id":18,"valueitems":[{"specid":5152,"value":"90.0"}]},{"name":"行李箱容积(L)","id":19,"valueitems":[{"specid":5152,"value":"500"}]},{"name":"前排宽度(mm)","id":100272,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"前排高度(mm)","id":100273,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"前排腿部空间最小值(mm)","id":100274,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"前排腿部空间最大值(mm)","id":100275,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"前排坐垫长度(mm)","id":100276,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"后排宽度(mm)","id":100277,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"后排高度(mm)","id":100278,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"后排腿部空间最小值(mm)","id":100279,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"后排腿部空间最大值(mm)","id":100280,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"后排坐垫长度(mm)","id":100281,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"后排中央地台高度(mm)","id":100282,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"后备箱开启后宽度(mm)","id":100283,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"后备箱开启后高度(mm)","id":100284,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"后备箱开启后纵向深度(mm)","id":100285,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"后备箱开启后放倒后排纵向深度(mm)","id":100286,"valueitems":[{"specid":5152,"value":"-"}]}]},{"typeId":3,"name":"发动机参数","paramitems":[{"name":"发动机型号","id":20,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"汽缸容积(cc)","id":21,"valueitems":[{"specid":5152,"value":"5998"}]},{"name":"工作方式","id":23,"valueitems":[{"specid":5152,"value":"自然吸气"}]},{"name":"汽缸排列形式","id":24,"valueitems":[{"specid":5152,"value":"W"}]},{"name":"汽缸数(个)","id":25,"valueitems":[{"specid":5152,"value":"12"}]},{"name":"每缸气门数(个)","id":26,"valueitems":[{"specid":5152,"value":"4"}]},{"name":"压缩比","id":27,"valueitems":[{"specid":5152,"value":"10.8"}]},{"name":"气门结构","id":28,"valueitems":[{"specid":5152,"value":"DOHC"}]},{"name":"缸径","id":29,"valueitems":[{"specid":5152,"value":"84.0"}]},{"name":"冲程","id":30,"valueitems":[{"specid":5152,"value":"90.2"}]},{"name":"最大马力(Ps)","id":31,"valueitems":[{"specid":5152,"value":"450"}]},{"name":"最大功率(kW)","id":32,"valueitems":[{"specid":5152,"value":"331"}]},{"name":"最大功率转速(rpm)","id":33,"valueitems":[{"specid":5152,"value":"6050"}]},{"name":"最大扭矩(N·m)","id":34,"valueitems":[{"specid":5152,"value":"560"}]},{"name":"最大扭矩转速(rpm)","id":35,"valueitems":[{"specid":5152,"value":"2750-5200"}]},{"name":"发动机特有技术","id":36,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"燃料形式","id":37,"valueitems":[{"specid":5152,"value":"汽油"}]},{"name":"燃油标号","id":38,"valueitems":[{"specid":5152,"value":"97号"}]},{"name":"供油方式","id":39,"valueitems":[{"specid":5152,"value":"直喷"}]},{"name":"缸盖材料","id":40,"valueitems":[{"specid":5152,"value":"铝"}]},{"name":"缸体材料","id":41,"valueitems":[{"specid":5152,"value":"铝"}]},{"name":"环保标准","id":42,"valueitems":[{"specid":5152,"value":"欧IV+OBD"}]}]},{"typeId":5,"name":"底盘转向参数","paramitems":[{"name":"驱动方式","id":45,"valueitems":[{"specid":5152,"value":"前置四驱"}]},{"name":"前悬挂类型","id":46,"valueitems":[{"specid":5152,"value":"多连杆独立悬架"}]},{"name":"后悬挂类型","id":47,"valueitems":[{"specid":5152,"value":"多连杆独立悬架"}]},{"name":"车体结构","id":49,"valueitems":[{"specid":5152,"value":"承载式"}]},{"name":"助力类型","id":48,"valueitems":[{"specid":5152,"value":"机械液压助力"}]},{"name":"四驱形式","id":100290,"valueitems":[{"specid":5152,"value":"全时四驱"}]},{"name":"中央差速器结构","id":100291,"valueitems":[{"specid":5152,"value":"托森式差速器"}]}]},{"typeId":6,"name":"车轮制动参数","paramitems":[{"name":"前制动器类型","id":50,"valueitems":[{"specid":5152,"value":"通风盘式"}]},{"name":"后制动器类型","id":51,"valueitems":[{"specid":5152,"value":"通风盘式"}]},{"name":"驻车制动类型","id":52,"valueitems":[{"specid":5152,"value":"脚刹"}]},{"name":"前轮胎规格","id":53,"valueitems":[{"specid":5152,"value":"245/45 R19"}]},{"name":"后轮胎规格","id":54,"valueitems":[{"specid":5152,"value":"245/45 R19"}]},{"name":"备胎规格","id":55,"valueitems":[{"specid":5152,"value":"无"}]}]}]}}$$$$$$$$$${"returncode":0,"message":"成功","result":{"seriesid":110,"configtypeitems":[{"typeId":7,"name":"安全装备","configitems":[{"name":"主/副驾驶座安全气囊","id":57,"valueitems":[{"specid":5152,"value":"主●/副●"}]},{"name":"前/后排侧气囊","id":58,"valueitems":[{"specid":5152,"value":"前●/后●"}]},{"name":"前/后排头部气囊(气帘)","id":60,"valueitems":[{"specid":5152,"value":"前●/后●"}]},{"name":"膝部气囊","id":62,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"胎压监测装置","id":63,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"安全带未系提示","id":65,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"零胎压继续行驶","id":64,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"车内中控锁","id":67,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"发动机电子防盗","id":66,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"遥控钥匙","id":68,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"无钥匙启动系统","id":69,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"儿童安全座椅合","id":100292,"valueitems":[{"specid":5152,"value":"●"}]}]},{"typeId":8,"name":"控制配置","configitems":[{"name":"制动防抱死系统(ABS)","id":70,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"制动力分配系统(EBD/CBC等)","id":71,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"制动辅助系统(EBA/BAS/BA等)","id":72,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"牵引力控制系统(ASR/TCS/TRC等)","id":73,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"车辆稳定控制系统(ESP/DSC/VSC等)","id":74,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"自动驻车/上坡辅助系统","id":75,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"陡坡缓降系统","id":76,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"可调悬挂","id":77,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"空气悬挂","id":78,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"主动转向系统","id":79,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"前桥限滑差速器/差速锁","id":100293,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"中央差速器锁止功能","id":100294,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"后桥限滑差速器/差速锁","id":100295,"valueitems":[{"specid":5152,"value":"-"}]}]},{"typeId":9,"name":"外部配置","configitems":[{"name":"电动/手动天窗","id":80,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"全景/电动全景天窗","id":81,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"运动外观套件","id":82,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"铝合金轮毂","id":83,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"电动吸合门","id":84,"valueitems":[{"specid":5152,"value":"●"}]}]},{"typeId":10,"name":"内部配置","configitems":[{"name":"真皮方向盘","id":85,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"方向盘调节","id":86,"valueitems":[{"specid":5152,"value":"上下+前后调节"}]},{"name":"方向盘电动调节","id":88,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"多功能方向盘","id":89,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"方向盘换挡","id":90,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"定速巡航","id":91,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"倒车辅助/倒车雷达","id":92,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"可视倒车辅助","id":93,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"行车电脑显示屏","id":94,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"风挡投射显示系统(HUD)","id":95,"valueitems":[{"specid":5152,"value":"-"}]}]},{"typeId":11,"name":"座椅配置","configitems":[{"name":"真皮/仿皮座椅","id":96,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"运动座椅","id":97,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"座椅高低调节","id":98,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"腰部支撑调节","id":99,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"肩部支撑调节","id":100,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"前排座椅电动调节","id":101,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"第二排靠背角度调节","id":102,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"第二排座椅前后调节","id":103,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"后排座椅电动调节","id":104,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"座椅记忆","id":105,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"前/后排座椅加热","id":106,"valueitems":[{"specid":5152,"value":"前●/后●"}]},{"name":"座椅通风","id":108,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"座椅按摩","id":109,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"后排座椅放倒方式","id":110,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"第三排座椅","id":112,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"前/后座中央扶手","id":113,"valueitems":[{"specid":5152,"value":"前●/后●"}]},{"name":"后排杯架","id":115,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"电动后备箱门","id":116,"valueitems":[{"specid":5152,"value":"●"}]}]},{"typeId":12,"name":"多媒体配置","configitems":[{"name":"车载GPS导航系统","id":117,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"定位互动服务系统","id":118,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"中控台彩色显示屏","id":119,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"车辆交互系统(iDrive/MMI等)","id":120,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"内置硬盘存储空间","id":121,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"蓝牙/车载电话","id":122,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"车载电视","id":123,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"后排液晶屏","id":124,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"外接音源接口(AUX/USB/iPod等)","id":125,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"CD支持MP3/WMA","id":126,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"多媒体系统","id":127,"valueitems":[{"specid":5152,"value":"多碟DVD●"}]},{"name":"2-3只扬声器","id":132,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"4-5只扬声器","id":133,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"6-7只扬声器","id":134,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"≥8只扬声器","id":135,"valueitems":[{"specid":5152,"value":"●"}]}]},{"typeId":13,"name":"灯光配置","configitems":[{"name":"氙气大灯","id":136,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"日间行车灯","id":137,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"自动大灯","id":138,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"前雾灯","id":140,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"随动转向大灯/转向辅助灯","id":139,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"大灯高度自动/手动可调","id":141,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"大灯清洗装置","id":142,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"车内氛围灯","id":143,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"LED大灯(不用了)","id":100296,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"LED大灯","id":210240,"valueitems":[{"specid":5152,"value":"-"}]}]},{"typeId":14,"name":"玻璃/后视镜","configitems":[{"name":"前/后电动车窗","id":144,"valueitems":[{"specid":5152,"value":"前●/后●"}]},{"name":"车窗防夹手功能","id":146,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"防紫外线/隔热玻璃","id":147,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"外后视镜电动调节","id":148,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"外后视镜电加热","id":149,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"外后视镜电动折叠","id":151,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"外后视镜记忆功能","id":152,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"后视镜自动防眩目","id":150,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"后风挡遮阳帘","id":153,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"后排侧遮阳帘","id":154,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"遮阳板化妆镜","id":155,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"后风挡雨刷","id":156,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"自动雨刷","id":157,"valueitems":[{"specid":5152,"value":"●"}]}]},{"typeId":15,"name":"空调/冰箱","configitems":[{"name":"空调控制方式","id":158,"valueitems":[{"specid":5152,"value":"自动●"}]},{"name":"后排独立空调","id":160,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"后座出风口","id":161,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"温度分区控制","id":162,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"空气净化/花粉过滤","id":163,"valueitems":[{"specid":5152,"value":"●"}]},{"name":"车载冰箱","id":164,"valueitems":[{"specid":5152,"value":"●"}]}]},{"typeId":16,"name":"高科技配置","configitems":[{"name":"自适应巡航系统","id":171,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"车辆行驶并线辅助系统","id":166,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"主动刹车/安全系统","id":167,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"整体主动转向系统","id":168,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"自动泊车辅助系统","id":165,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"可视夜视系统","id":169,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"中控液晶屏分屏显示","id":170,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"车辆全景影像系统","id":172,"valueitems":[{"specid":5152,"value":"-"}]}]},{"typeId":17,"name":"纯电动发动机参数","configitems":[{"name":"电池支持最高续航里程(km)","id":181,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"电池容量(kw/h)","id":182,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"电动机最大功率(kW)","id":186,"valueitems":[{"specid":5152,"value":"-"}]},{"name":"电动机最大扭矩(N*m)","id":187,"valueitems":[{"specid":5152,"value":"-"}]}]}]}}'
    return HttpResponse(content_pos)