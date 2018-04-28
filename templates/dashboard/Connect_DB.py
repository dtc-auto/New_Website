# -*- coding: utf-8 -*-
from __future__ import unicode_literals,division
import pymssql
import pandas as pd
import urllib

server = "SQLDEV02\sql"
server = "127.0.0.1"
user = "dtc"
password = "asdf1234"


def getCarOwner(para):
    sql = '''
        SELECT 
             w.Brand
            ,m.province
            ,COUNT(m.province) AS no
        FROM 
            DW_AutoHome_WOM AS w INNER JOIN
            DM_VW_region AS r ON w.City = r.City INNER JOIN
            DM_AutoHome_Map AS m ON m.province = r.Province
        GROUP BY 
              w.Brand
             ,m.province
        ORDER BY 
            no desc
        '''
    conn = pymssql.connect(server, user, password, "BDCI")
    df = pd.read_sql_query(sql, conn)
    brand = u'帕萨特'
    df = df.loc[df['Brand'] == para]
    result = [['province', 'no']]
    proList = df['province'].tolist()
    noList = df['no'].tolist()
    max_data = 0
    for i in range(0, len(noList)):
        pro = proList[i]
        no = noList[i]
        if int(no) > max_data:
            max_data = int(no)
        dit_ = {'name': pro, 'value': int(no)}
        result.append(dit_)
    re_list = result[1:]

    return re_list, max_data
# a,b = getCarOwner(u'凯美瑞')

def getColumnChart_p1():
    sql = """
            SELECT 
                 w.brand
                ,r.Region
                ,count(w.brand) as no
            FROM 
                BDCI.dbo.DW_AutoHome_WOM AS w INNER JOIN
                BDCI.dbo.DM_VW_region AS r ON w.City = r.City
            GROUP BY
                w.brand,r.Region
            ORDER BY
                w.brand
            """
    conn = pymssql.connect(server, user, password, "BDCI")
    df = pd.read_sql_query(sql, conn)
    result = [['brand','东北区','华北区','华东区','华南区','华中区','西区']]
    brandList = list(set(df['brand'].tolist()))
    for i in range(0,len(brandList)):
        df_temp = df.loc[df['brand'] == brandList[i]]
        list_temp = df_temp['no'].tolist()
        subresult = [brandList[i]]
        # 保留两位有效数字

        sum_temp = sum(list_temp)
        for no in list_temp:
            subresult.append(no/sum_temp)
        result.append(subresult)
    # 保留3位小数
    for i_list in range(1, len(result)):
        for i_ in range(1, len(result[i_list])):
            # print(result[i_list])
            result[i_list][i_] = float('%.3f'% result[i_list][i_])
    return result
# getColumnChart_p1()

def getLevel1Attributes(paraList):
    newList = paraList.strip('[]').replace('"','').split(',')
    conn = pymssql.connect(server, user, password, "BDCI")
    sql = """
            SELECT 
                 avg(score) as Score
                ,Aspect
                ,Brand
            FROM 
                DW_indexevaluationunpivot
            GROUP BY 
                Brand,aspect
            ORDER BY 
                Aspect asc
            """
    df = pd.read_sql_query(sql, conn)
    #print df.head()
    target = newList
    #target = ['凯美瑞', '帕萨特']
    data_list = []
    aspect_list = ['Comfort','Controllability','Cost performance','Exterior','Fuel Consumption','Interior','Power','Space']
    data_list.append(aspect_list)
    result = []
    for brand_index in range(0, len(target)):
        sub = (target[brand_index])
        df_temp = df.loc[df['Brand'] == sub]
        scorelist = df_temp['Score'].tolist()
        result.append(scorelist)
    # 标记数据为快速实现echart 暂时注释掉
    # for i in range(0,8):
        # result[i].insert(0,aspect_list[i].encode('utf8'))
    # [x.encode('utf8') for x in target]
    #print type(target[0])
    # target.insert(0,'Aspect'.encode('utf8'))

    result.insert(0,target)
    # 保留两位小数
    for i_list in range(1, len(result)):
        for i_ in range(0, len(result[i_list])):
            # print(result[i_list])
            result[i_list][i_] = float('%.2f'% result[i_list][i_])
    return result
# getLevel1Attributes("凯美瑞,帕萨特,雅阁,迈锐宝,迈锐宝XL,迈腾,蒙迪欧,名图")

def getLevel2Attributes(paraList):
    list1 = paraList.strip('[]')
    list2 = list1.replace('"','')
    list3 = list2.split(',')
    conn = pymssql.connect(server, user, password, "BDCI")
    sql = """
            USE BDCI
            SELECT  
                 Brand
                ,Dimension
                ,keyindex
                ,KeyModifier
                ,SentenceAttitude
                ,case when SentenceAttitude >= 1 then '1'
            WHEN 
                SentenceAttitude = 0 then '0'
            WHEN
                SentenceAttitude <= -1 then '-1' end  
            AS
                 Attitude
                ,frequency
            FROM 
                DM_AutoHome_WOM_SecondLevelIndex_Noun_Modifier_Attitude_Frequency
            WHERE 
                updateflag=0 and keyindex!='老板键' 
            ORDER BY 
                keyindex desc 
            """
    df = pd.read_sql_query(sql, conn)
    #brand = u'帕萨特'
    #dimension = u'操控'
    brand = list3[0]
    dimension = list3[1]
    df = df.loc[df['Brand'] == brand]
    df = df.loc[df['Dimension'] == dimension]
    indexList = df['keyindex'].tolist()
    indexList_de_weight = list(set(indexList))  # 列表去重（乱序）
    indexList_de_weight.sort(key=indexList.index)  # 恢复列表次序
    indexList = indexList_de_weight
    result = []
    title = ['index', '满意', '没感觉', '不满意']
    result.append(title)
    for index in indexList:
        manyiCount = 0
        meiganjueCount = 0
        bumanyiCount = 0
        sum_list = []
        attitudeList = df.loc[df['keyindex'] == index]['Attitude'].tolist()
        for attitude in attitudeList:
            if attitude == '1':
                manyiCount += 1
            elif attitude == '0':
                meiganjueCount += 1
            else:
                bumanyiCount += 1
        subResult = [index, manyiCount, meiganjueCount, bumanyiCount]
        result.append(subResult)
    result_return = result[0:10]
    # 返回值排序
    for key in range(1, len(result_return)):
        sum_ = result_return[key][1]+result_return[key][2]+result_return[key][3]
        sum_list.append(sum_)

    dit_order = dict(zip(indexList[:10], sum_list))
    dit_order = sorted(dit_order.items(), key=lambda d: d[1])
    order_list = []
    for tup in dit_order:
        order_list.append(tup[0])  # 得到list顺序
    # result_return = sorted(result_return[1:], key=order_list.index)
    retuen_list_ = []
    retuen_list = []
    for key in range(0, len(order_list)):
        for value in result_return:
            if order_list[key] == value[0]:
                retuen_list_=[order_list[key]]
                retuen_list_.append(value[1])
                retuen_list_.append(value[2])
                retuen_list_.append(value[3])
                retuen_list.append(retuen_list_)
    retuen_list = [title] + retuen_list
    return retuen_list
getLevel2Attributes("凯美瑞,空间")

def getPurpose(para):
    sql = """
        SELECT 
             [ForCrossCountry]
            ,[ForRacing]
            ,[ForCarry]
            ,[ForBusiness]
            ,[ForGirls]
            ,[ForLongDistance]
            ,[ForChild] 
            ,[ForShopping]
            ,[ForSelfDriving]
            ,[ForWork]
            ,[Brand]
        FROM 
            [BDCI].[dbo].[DM_AutoHoome_Purpose]
         """
    conn = pymssql.connect(server, user, password, "BDCI")
    df = pd.read_sql_query(sql, conn)
    headers = list(df)
    df['sum'] = df.sum(axis=1)
    df.loc[-1] = df.sum(axis=0)
    for i in range(0,len(headers)-1):
        newHeader = headers[i]+'Per'
        df[newHeader] = df[headers[i]]/df['sum']
    indexes = df.index.values.tolist()
    averageList = df.loc[indexes[-1]].tolist()[12:22]
    #brand = u'帕萨特'
    df = df.loc[df['Brand']== para].iloc[:,12:22]
    result = []
    result.append(['Purpose','average',para])
    dataList = df.iloc[0].tolist()
    for i in range(0,len(headers)-1):
        averageData = averageList[i]
        data = dataList[i]
        header = headers[i]
        subResult = [header,averageData,data]
        result.append(subResult)
    #add average data
    for i_list in range(1, len(result)):
        for i_ in range(1, len(result[i_list])):
            # print(result[i_list])
            value_ = float('%.3f' % result[i_list][i_])
            result[i_list][i_] = (round(value_ * 100))
    return result
# getPurpose('凯美瑞')
# people_page  0:age, 1:gender, 2:region, 3:city leve
def people_get_pie(company):
    # 大众静态数据
    dit_VW = [
        # age
        [{'value': 9, 'name': '<=25'},
         {'value': 27, 'name': '26-30'},
         {'value': 27, 'name': '31-35'},
         {'value': 23, 'name': '36-40'},
         {'value': 14, 'name': '>40'}],
        # gender
        [{'value': 9, 'name': 'Male'},
         {'value': 91, 'name': 'Female'}],
        # region
        [{'value': 9, 'name': 'Northeast'},
         {'value': 24, 'name': 'North'},
         {'value': 24, 'name': 'East'},
         {'value': 24, 'name': 'South'},
         {'value': 10, 'name': 'Central'},
         {'value': 9, 'name': 'West'}],
        # city leve
        [{'value': 46, 'name': 'Tier1'},
         {'value': 22, 'name': 'Tier2'},
         {'value': 20, 'name': 'Tier3'},
         {'value': 4, 'name': 'Tier4'},
         {'value': 6, 'name': 'Tier5'},
         {'value': 2, 'name': 'Tier6'}]
        ]
    # 宝马静态数据
    dit_BMW = [
        # age
        [{'value': 12, 'name': '<=25'},
         {'value': 38, 'name': '26-30'},
         {'value': 44, 'name': '31-35'},
         {'value': 0, 'name': '36-40'},
         {'value': 6, 'name': '>40'}],
        # gender
        [{'value': 57, 'name': 'Male'},
         {'value': 43, 'name': 'Female'}],
        # region
        [{'value': 8, 'name': 'Northeast'},
         {'value': 29, 'name': 'North'},
         {'value': 18, 'name': 'East'},
         {'value': 16, 'name': 'South'},
         {'value': 14, 'name': 'Central'},
         {'value': 15, 'name': 'West'}],
        # city leve
        [{'value': 42, 'name': 'Tier1'},
         {'value': 15, 'name': 'Tier2'},
         {'value': 11, 'name': 'Tier3'},
         {'value': 10, 'name': 'Tier4'},
         {'value': 10, 'name': 'Tier5'},
         {'value': 12, 'name': 'Tier6'}]
        ]
    if company == 'VW':
        return dit_VW

    if company == 'BMW':
        return dit_BMW

# =======================修改部分=============================
def people_get_path(all_):
    try:
        test_ = int(all_[1])  # 防止sql注入
    except:
        return 0

    root_name = all_[1]
    # all_ = all_[0]
    path_data = {
        "nodes": [],
        "links": [],
        "type": "force",
    }

    sql = """select father_node as source, id as target, user_name as name
        from [BDCI].[dbo].[DW_Weibo_RepostPath]
        where root = 
        """+str(all_[1])
    # 3890290613886669、  3908444761689053：300

    # 3908011552343259、  3909125471922420：500、  3867692458956092：300
    conn = pymssql.connect(server, user, password, "BDCI")
    df = pd.read_sql_query(sql, conn)
    sourceList = df['source'].tolist()
    targetList = df['target'].tolist()
    nameList = df['name'].tolist()
    dic_number_id = dict(zip(targetList, nameList))
    dic_number_id[root_name] = all_[0]
    # 将数字name替换为中文
    def change_ch(targetList):
        for i in range(0, len(targetList)):
            for key in dic_number_id.keys():
                if key == targetList[i]:
                    targetList[i] = dic_number_id[key]
    change_ch(sourceList)
    change_ch(targetList)
    # 去重
    allName = list(set(sourceList+targetList))
    # 添加nodes:[{"name": "allName[0]",itemStyle:{normal:{color:'green'}},]
    for i in range(0, len(allName)):
        name_ = allName[i]
        if name_ == all_[0]:
            dit_ = {'name': name_, 'itemStyle': {'normal': {'color': 'rgb(255,0,0)'}}}
            path_data["nodes"].append(dit_)
        else:
            dit_ = {'name': name_, 'itemStyle': {'normal': {'color': 'rgb(18,39,105)'}}}
            path_data["nodes"].append(dit_)

    # 添加links
    for i in range(0, len(sourceList)):
        dit_ = {
            "source": sourceList[i],
            "target": targetList[i]
        }
        path_data["links"].append(dit_)

    return path_data
# people_get_path(['BMW','3718567394161044'])

# 返回微博内容：因为本地无原始表数据，所以只用2条微博做示范，可自由增加id（root）与text个数
def people_get_text(company):

    text_bmw = [
        ['3718567394161044', '3908444761689053'],
        ['新BMW X1 行动定义自由 新BMW X1，作为同级唯一全系标准配备高端动力配置的车型，用10款车型为客户提供更多高端舒适体验',
         'BMW X1自由能量，即将全力爆发。 ​​​​'
         ]
    ]
    text_vw = [
        ['3898167562657684', '3855030983972696'],
        ['不仅仅是油电混合，更是满足你出行的多种选择。全新Golf GTE让你动静随芯选',
         '凌风渡越，颠覆想象。沿袭前瞻造车理念，大众汽车凌渡以全新轿跑个性之魅，颠覆时尚美学。极致横向拓展前脸，配合动感氙气大灯，为整车勾勒出简洁流畅的外观线条。'
         ]
    ]
    if company == 'BMW':
        return text_bmw
    else:
        return text_vw

    # =======================修改部分=============================
# CP_page
def CP_get_cluster():
    sql = """
        SELECT 
             value
            ,slevel
        FROM 
            [BDCI].[dbo].[Source_Weibo_Cluster]
        """
    conn = pymssql.connect(server, user, password, "BDCI")
    df = pd.read_sql_query(sql, conn)
    x = df['value'].tolist()
    y = df['slevel'].tolist()
    cluster_data = []
    for i in range(len(x)):
        x_ = round(float(x[i])*10, 2)
        y_ = round(float(y[i])*10, 2)
        if 0 < x_ <= 10 and 0 < y_ <= 10:
            ele = [x_, y_]
            cluster_data.append(ele)
    return cluster_data

# ConfigPage_page
def Config_get_config(id_):
    url_pos = "http://auto.chexun.com/singleModledata.do?modelId={0}".format(id_)
    result_pos = urllib.request.urlopen(url_pos)  # POST method
    content_pos = result_pos.read().strip().decode('utf-8')
    return content_pos



# 车系选择框列表
def Config_get_company(id_):
    id_ = int(id_)  # 防止SQL注入

    sql = """
            SELECT 
                 [SERIE_ID]
                ,[SERIE_NAME_CN]
                ,[COMPANY_ID]
                ,[COMPANY_NAME_CN]
            FROM 
                [BDCI_CHEXUN].[stg].[CONFIG_KEY_2018_01_30] 
            WHERE
                BRAND_ID="""+str(id_)+"""
            """
    conn = pymssql.connect(server, user, password, "BDCI")
    df = pd.read_sql_query(sql, conn)

    re_list = [] # 返回列表

    company_dic = {
        "companyId": "",
        "companyName": "",
        "seriesList": []
    } # 第一层嵌套 公司
    series_dic = {
        "seriesId": "",
        "seriesName": ""
    } # 第二次嵌套 车系

    SERIE_ID = df['SERIE_ID'].tolist()
    SERIE_NAME = df['SERIE_NAME_CN'].tolist()
    COMPANY_ID = df['COMPANY_ID'].tolist()
    COMPANY_NAME_CN = df['COMPANY_NAME_CN'].tolist()

    dic_serie = dict(zip(SERIE_ID, SERIE_NAME))
    dic_company = dict(zip(COMPANY_ID, COMPANY_NAME_CN))
    dic_key_id = dict(zip(SERIE_ID, COMPANY_ID))
    for company_id in dic_company.keys():
        company_dic = {
            "companyId": "",
            "companyName": "",
            "seriesList": []
        }
        company_dic["companyId"] = company_id
        company_dic["companyName"] = dic_company[company_id]
        for series_id in SERIE_ID:
            if company_id == dic_key_id[series_id]:
                # print(company_id, dic_key_id[series_id], series_id)
                series_dic = {
                    "seriesId": "",
                    "seriesName": ""
                }
                series_dic["seriesId"] = series_id
                series_dic["seriesName"] = dic_serie[series_id]
                company_dic["seriesList"].append(series_dic)
        re_list.append(company_dic)
    return re_list

# Config_get_company(23)

# 车型选择框
def Config_get_model(id_):
    id_ = int(id_)  # 防止SQL注入

    sql = """  
            SELECT 
                 车型名称
                ,年代款
                ,SPEC_ID
            FROM 
                [BDCI_CHEXUN].[stg].[CONFIG_KEY_SERIE_SPEC] 
            WHERE 
                [车型名称] 
            IN( 
                SELECT 
                [车型名称]
                FROM 
                [BDCI_CHEXUN].[stg].[CONFIG_KEY_SERIE_SPEC] 
                GROUP BY 
                [车型名称] having count([车型名称]) = 1 )
            AND
                SERIE_ID=""" + str(id_) + """
            GROUP BY 年代款,车型名称,SPEC_ID
            """
    conn = pymssql.connect(server, user, password, "BDCI")
    df = pd.read_sql_query(sql, conn)

    re_list = []  # 返回列表

    year_dic = {
        "yearId": "",
        "yearName": "",
        "modelList": []
    }  # 第一层嵌套 年份
    model_dic = {
        "modelId": "",
        "modelName": ""
    }  # 第二次嵌套 车型

    MODEL_NAME = df['车型名称'].tolist()
    SPEC_ID = df['SPEC_ID'].tolist()
    YEAR_NAME = df['年代款'].tolist()
    YEAR_ID = df['年代款'].tolist()  # 设置year_id=year_name

    dic_model = dict(zip(SPEC_ID, MODEL_NAME))
    dic_year = dict(zip(YEAR_NAME, YEAR_ID))
    dic_key_id = dict(zip(SPEC_ID, YEAR_ID))
    for year_id in dic_year.keys():
        year_dic = {
            "yearId": "",
            "yearName": "",
            "modelList": []
        }
        year_dic["yearId"] = year_id
        year_dic["yearName"] = dic_year[year_id]
        for spec_id in SPEC_ID:
            if year_id == dic_key_id[spec_id]:
                model_dic = {
                    "modelId": "",
                    "modelName": ""
                }
                model_dic["modelId"] = spec_id
                model_dic["modelName"] = dic_model[spec_id]
                year_dic["modelList"].append(model_dic)
        re_list.append(year_dic)
    return re_list

# Config_get_model(104224)

# 读取配置数据
def Config_get_config_local(id_):
    id_ = int(id_)
    sql = """
            SELECT 
                 [BDCI_CHEXUN].[stg].[CONFIGURATION_DETAILS].[PARA_NAME]
                ,[PARA_VALUE]
            FROM 
                [BDCI_CHEXUN].[stg].[CONFIGURATION_DETAILS]
            JOIN 
                [BDCI_CHEXUN].[stg].[CONFIG_ITEM]
            ON
                [BDCI_CHEXUN].[stg].[CONFIGURATION_DETAILS].[PARA_NAME]=[BDCI_CHEXUN].[stg].[CONFIG_ITEM].[PARA_NAME]
            WHERE 
                [SPEC_ID]="""+str(id_)+"""
            ORDER BY 
                convert (int,PARA_ID)
            """
    conn = pymssql.connect(server, user, password, "BDCI")
    df = pd.read_sql_query(sql, conn)
    name = df['PARA_NAME'].tolist()
    value = df['PARA_VALUE'].tolist()
    dic_template = {	"基础参数":[
		"车型名称","年代款","厂商指导价","全国经销商最低价","实测100-0制动（m）","官方0-100加速（s）","实测油耗（L）","最高车速（km/h）","工信部综合油耗（L）",
		"排量(L)","长*宽*高(mm)","整车质保","车身结构","挡位个数","变速箱类型"],"车身参数":[
		"轴距(mm)","前轮距(mm)","后轮距(mm)","最小离地间隙(mm)","整备质量(Kg)","车门数(个)","座位数(个)","油箱容积(L)","行李箱容积(L)","前排宽度(mm)",
		"前排高度(mm)","前排腿部空间最小值(mm)","前排腿部空间最大值(mm)","前排坐垫长度(mm)","后排宽度(mm)","后排高度(mm)","后排腿部空间最小值(mm)","后排腿部空间最大值(mm)",
		"后排坐垫长度(mm)","后排中央地台高度(mm)","后备箱开启后宽度(mm)","后备箱开启后高度(mm)","后备箱开启后纵向深度(mm)","后备箱开启后放倒后排纵向深度(mm)"],"发动机参数":["发动机型号","汽缸容积(cc)","工作方式","汽缸排列形式","汽缸数(个)","每缸气门数(个)","压缩比","气门结构","缸径","冲程","最大马力(Ps)",
		"最大功率(kW)","最大功率转速(rpm)","最大扭矩(N·m)","最大扭矩转速(rpm)","发动机特有技术","燃料形式","燃油标号","供油方式","缸盖材料","缸体材料","环保标准"],"底盘转向参数":[
		"驱动方式","前悬挂类型","后悬挂类型","车体结构","助力类型","四驱形式","中央差速器结构"],"车轮制动参数":[
		"前制动器类型","后制动器类型","驻车制动类型","前轮胎规格","后轮胎规格","备胎规格"],"安全装备": [
		"主/副驾驶座安全气囊","前/后排侧气囊","前/后排头部气囊(气帘)","膝部气囊","胎压监测装置","安全带未系提示","零胎压继续行驶","车内中控锁",
		"发动机电子防盗","遥控钥匙","无钥匙启动系统","儿童安全座椅合"],"控制配置":[
		"制动防抱死系统(ABS)","制动力分配系统(EBD/CBC等)","制动辅助系统(EBA/BAS/BA等)","牵引力控制系统(ASR/TCS/TRC等)","车辆稳定控制系统(ESP/DSC/VSC等)",
		"自动驻车/上坡辅助系统","陡坡缓降系统","可调悬挂","空气悬挂","主动转向系统","前桥限滑差速器/差速锁","中央差速器锁止功能","后桥限滑差速器/差速锁"],"外部配置":[
		"电动/手动天窗","全景/电动全景天窗","运动外观套件","铝合金轮毂","电动吸合门"],"内部配置":[
		"真皮方向盘","方向盘调节","方向盘电动调节","多功能方向盘","方向盘换挡","定速巡航","倒车辅助/倒车雷达","可视倒车辅助","行车电脑显示屏","风挡投射显示系统(HUD)"],
                            "座椅配置":[
		"真皮/仿皮座椅","运动座椅","座椅高低调节","腰部支撑调节","肩部支撑调节","前排座椅电动调节","第二排靠背角度调节","第二排座椅前后调节","后排座椅电动调节",
		"座椅记忆","前/后排座椅加热","座椅通风","座椅按摩","后排座椅放倒方式","第三排座椅","前/后座中央扶手","后排杯架","电动后备箱门"],"多媒体配置":[
		"车载GPS导航系统","定位互动服务系统","中控台彩色显示屏","车辆交互系统(iDrive/MMI等)","内置硬盘存储空间","蓝牙/车载电话","车载电视","后排液晶屏","外接音源接口(AUX/USB/iPod等)",
		"CD支持MP3/WMA","多媒体系统","2-3只扬声器","4-5只扬声器","6-7只扬声器","≥8只扬声器"],"灯光配置":[
		"氙气大灯","日间行车灯","自动大灯","前雾灯","随动转向大灯/转向辅助灯","大灯高度自动/手动可调","大灯清洗装置","车内氛围灯","LED大灯"],"玻璃/后视镜":[
		"前/后电动车窗","车窗防夹手功能","防紫外线/隔热玻璃","外后视镜电动调节","外后视镜电加热","外后视镜电动折叠","外后视镜记忆功能","后视镜自动防眩目","后风挡遮阳帘",
		"后排侧遮阳帘","遮阳板化妆镜","后风挡雨刷","自动雨刷"],"空调/冰箱":[
		"空调控制方式","后排独立空调","后座出风口","温度分区控制","空气净化/花粉过滤","车载冰箱"],"高科技配置":[
		"自适应巡航系统","车辆行驶并线辅助系统","主动刹车/安全系统","整体主动转向系统","自动泊车辅助系统","可视夜视系统","中控液晶屏分屏显示","车辆全景影像系统"],"纯电动发动机参数":[
		"电池支持最高续航里程(km)","电池容量(kw/h)","电动机最大功率(kW)","电动机最大扭矩(N*m)"]
    }
    list_order = [	"基础参数",
		"车型名称","年代款","厂商指导价","全国经销商最低价","实测100-0制动（m）","官方0-100加速（s）","实测油耗（L）","最高车速（km/h）","工信部综合油耗（L）",
		"排量(L)","长*宽*高(mm)","整车质保","车身结构","挡位个数","变速箱类型",

	"车身参数",
		"轴距(mm)","前轮距(mm)","后轮距(mm)","最小离地间隙(mm)","整备质量(Kg)","车门数(个)","座位数(个)","油箱容积(L)","行李箱容积(L)","前排宽度(mm)",
		"前排高度(mm)","前排腿部空间最小值(mm)","前排腿部空间最大值(mm)","前排坐垫长度(mm)","后排宽度(mm)","后排高度(mm)","后排腿部空间最小值(mm)","后排腿部空间最大值(mm)",
		"后排坐垫长度(mm)","后排中央地台高度(mm)","后备箱开启后宽度(mm)","后备箱开启后高度(mm)","后备箱开启后纵向深度(mm)","后备箱开启后放倒后排纵向深度(mm)",

	"发动机参数",
		"发动机型号","汽缸容积(cc)","工作方式","汽缸排列形式","汽缸数(个)","每缸气门数(个)","压缩比","气门结构","缸径","冲程","最大马力(Ps)",
		"最大功率(kW)","最大功率转速(rpm)","最大扭矩(N·m)","最大扭矩转速(rpm)","发动机特有技术","燃料形式","燃油标号","供油方式","缸盖材料","缸体材料","环保标准",

	"底盘转向参数",
		"驱动方式","前悬挂类型","后悬挂类型","车体结构","助力类型","四驱形式","中央差速器结构",

	"车轮制动参数",
		"前制动器类型","后制动器类型","驻车制动类型","前轮胎规格","后轮胎规格","备胎规格",

	"安全装备",
		"主/副驾驶座安全气囊","前/后排侧气囊","前/后排头部气囊(气帘)","膝部气囊","胎压监测装置","安全带未系提示","零胎压继续行驶","车内中控锁",
		"发动机电子防盗","遥控钥匙","无钥匙启动系统","儿童安全座椅合",

	"控制配置",
		"制动防抱死系统(ABS)","制动力分配系统(EBD/CBC等)","制动辅助系统(EBA/BAS/BA等)","牵引力控制系统(ASR/TCS/TRC等)","车辆稳定控制系统(ESP/DSC/VSC等)",
		"自动驻车/上坡辅助系统","陡坡缓降系统","可调悬挂","空气悬挂","主动转向系统","前桥限滑差速器/差速锁","中央差速器锁止功能","后桥限滑差速器/差速锁",

	"外部配置",
		"电动/手动天窗","全景/电动全景天窗","运动外观套件","铝合金轮毂","电动吸合门",

	"内部配置",
		"真皮方向盘","方向盘调节","方向盘电动调节","多功能方向盘","方向盘换挡","定速巡航","倒车辅助/倒车雷达","可视倒车辅助","行车电脑显示屏","风挡投射显示系统(HUD)",

	"座椅配置",
		"真皮/仿皮座椅","运动座椅","座椅高低调节","腰部支撑调节","肩部支撑调节","前排座椅电动调节","第二排靠背角度调节","第二排座椅前后调节","后排座椅电动调节",
		"座椅记忆","前/后排座椅加热","座椅通风","座椅按摩","后排座椅放倒方式","第三排座椅","前/后座中央扶手","后排杯架","电动后备箱门",

	"多媒体配置",
		"车载GPS导航系统","定位互动服务系统","中控台彩色显示屏","车辆交互系统(iDrive/MMI等)","内置硬盘存储空间","蓝牙/车载电话","车载电视","后排液晶屏","外接音源接口(AUX/USB/iPod等)",
		"CD支持MP3/WMA","多媒体系统","2-3只扬声器","4-5只扬声器","6-7只扬声器","≥8只扬声器",

	"灯光配置",
		"氙气大灯","日间行车灯","自动大灯","前雾灯","随动转向大灯/转向辅助灯","大灯高度自动/手动可调","大灯清洗装置","车内氛围灯","LED大灯",

	"玻璃/后视镜",
		"前/后电动车窗","车窗防夹手功能","防紫外线/隔热玻璃","外后视镜电动调节","外后视镜电加热","外后视镜电动折叠","外后视镜记忆功能","后视镜自动防眩目","后风挡遮阳帘",
		"后排侧遮阳帘","遮阳板化妆镜","后风挡雨刷","自动雨刷",

	"空调/冰箱",
		"空调控制方式","后排独立空调","后座出风口","温度分区控制","空气净化/花粉过滤","车载冰箱",

	"高科技配置",
		"自适应巡航系统","车辆行驶并线辅助系统","主动刹车/安全系统","整体主动转向系统","自动泊车辅助系统","可视夜视系统","中控液晶屏分屏显示","车辆全景影像系统",

	"纯电动发动机参数",
		"电池支持最高续航里程(km)","电池容量(kw/h)","电动机最大功率(kW)","电动机最大扭矩(N*m)"
]
    dic_use = dict(zip(name, value))
    list_value = []
    re_list_m = []
    list_name = []
    k = []

    for name_ in list_order:
        for name__ in dic_use.keys():
            if name_ == name__:
                list_value.append(dic_use[name_])

    for key in dic_template.keys():
        list_name = list_name+dic_template[key]

    for i in list_order:
        if i in list_name:
            re_list_m.append('')
        else:
            re_list_m.append(i)

    # 删除多余行
    for i in range(len(re_list_m)-16):
        if re_list_m[i] is not "":
            del re_list_m[i+1]

    # 空值替换为name的类
    for i in range(len(re_list_m)):
        if re_list_m[i] != '':
            target = re_list_m[i]
        else:
            re_list_m[i] = target

    for key in dic_template.keys():
        k.append(key)

    re_dic_ = {"name": list_name, "value": list_value, "m": re_list_m, "k": k}
    return re_dic_

# Config_get_config_local(108517)

# 二手车评估
# 车系选择框列表
def Price_get_company(id_):
    id_ = int(id_)  # 防止SQL注入

    sql = """
            SELECT 
                 [SERIE_ID]
                ,serie as [SERIE_NAME_CN]
                ,[COMPANY_ID]
                ,company as [COMPANY_NAME_CN]
            FROM 
                [BDCI_AUTOHOME_new].[src].[AutoHome_Price_Specs_Forweb]
            WHERE
                BRAND_ID="""+str(id_)+"""
            """
    conn = pymssql.connect(server, user, password, "BDCI")
    df = pd.read_sql_query(sql, conn)

    re_list = [] # 返回列表

    company_dic = {
        "companyId": "",
        "companyName": "",
        "seriesList": []
    } # 第一层嵌套 公司
    series_dic = {
        "seriesId": "",
        "seriesName": ""
    } # 第二次嵌套 车系

    SERIE_ID = df['SERIE_ID'].tolist()
    SERIE_NAME = df['SERIE_NAME_CN'].tolist()
    COMPANY_ID = df['COMPANY_ID'].tolist()
    COMPANY_NAME_CN = df['COMPANY_NAME_CN'].tolist()

    def delRepeat(liebiao):
        for x in liebiao:
            while liebiao.count(x) > 1:
                del liebiao[liebiao.index(x)]
        return liebiao


    dic_serie = dict(zip(SERIE_ID, SERIE_NAME))
    dic_company = dict(zip(COMPANY_ID, COMPANY_NAME_CN))
    dic_key_id = dict(zip(SERIE_ID, COMPANY_ID))
    for company_id in dic_company.keys():
        company_dic = {
            "companyId": "",
            "companyName": "",
            "seriesList": []
        }
        company_dic["companyId"] = company_id
        company_dic["companyName"] = dic_company[company_id]
        for series_id in SERIE_ID:
            if company_id == dic_key_id[series_id]:
                # print(company_id, dic_key_id[series_id], series_id)
                series_dic = {
                    "seriesId": "",
                    "seriesName": ""
                }
                series_dic["seriesId"] = series_id
                series_dic["seriesName"] = dic_serie[series_id]
                company_dic["seriesList"].append(series_dic)
        re_list.append(company_dic)
        for i in re_list:
            i['seriesList']=delRepeat(i['seriesList'])
    return re_list

# Price_get_company(2)

# 车型选择框
def Price_get_specl(id_):
    id_ = int(id_)  # 防止SQL注入

    sql = """  
            SELECT 
                 spec_name as 车型名称
                ,year as 年代款
                ,SPEC_ID
            FROM 
                [BDCI_AUTOHOME_new].[src].[AutoHome_Price_Specs_Forweb]
            WHERE 
                SERIE_ID=""" + str(id_) + """
            GROUP BY year,spec_name,SPEC_ID
            """
    conn = pymssql.connect(server, user, password, "BDCI")
    df = pd.read_sql_query(sql, conn)

    re_list = []  # 返回列表

    year_dic = {
        "yearId": "",
        "yearName": "",
        "modelList": []
    }  # 第一层嵌套 年份
    model_dic = {
        "modelId": "",
        "modelName": ""
    }  # 第二次嵌套 车型

    MODEL_NAME = df['车型名称'].tolist()
    SPEC_ID = df['SPEC_ID'].tolist()
    YEAR_NAME = df['年代款'].tolist()
    YEAR_ID = df['年代款'].tolist()  # 设置year_id=year_name

    dic_model = dict(zip(SPEC_ID, MODEL_NAME))
    dic_year = dict(zip(YEAR_NAME, YEAR_ID))
    dic_key_id = dict(zip(SPEC_ID, YEAR_ID))
    for year_id in dic_year.keys():
        year_dic = {
            "yearId": "",
            "yearName": "",
            "modelList": []
        }
        year_dic["yearId"] = year_id
        year_dic["yearName"] = dic_year[year_id]
        for spec_id in SPEC_ID:
            if year_id == dic_key_id[spec_id]:
                model_dic = {
                    "modelId": "",
                    "modelName": ""
                }
                model_dic["modelId"] = spec_id
                model_dic["modelName"] = dic_model[spec_id]
                year_dic["modelList"].append(model_dic)
        re_list.append(year_dic)
    return re_list

# Price_get_specl(11295)

# 计算二手车数值
def Price_get_pricel(id_):
    id_ = int(id_)  # 防止SQL注入

    sql = """  
            SELECT 
                 price
            FROM 
                [BDCI_AUTOHOME_new].[src].[AutoHome_Price_Specs_Forweb]
            WHERE 
                SPEC_ID=""" + str(id_) + """
            """
    conn = pymssql.connect(server, user, password, "BDCI")
    df = pd.read_sql_query(sql, conn)
    price = df['price'].tolist()[0][:-1]
    return price
Price_get_pricel(16385)