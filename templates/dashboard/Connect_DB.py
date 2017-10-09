# -*- coding: utf-8 -*-
from __future__ import unicode_literals,division
import pymssql
import pandas as pd

server = "sqldev02\sql"
user = "dtc"
password = "asdf1234"


def getCarOwner(para):
    # sql = """SELECT w.Brand, m.province_pinyin, COUNT(m.province_pinyin) AS no
    #          FROM DW_AutoHome_WOM AS w INNER JOIN
    #          DM_VW_region AS r ON w.City = r.City INNER JOIN
    #          DM_AutoHome_Map AS m ON m.province = r.Province
    #          GROUP BY w.Brand, m.province_pinyin
    #          ORDER BY no desc
    #          """
    sql = '''SELECT w.Brand, m.province, COUNT(m.province) AS no
             FROM DW_AutoHome_WOM AS w INNER JOIN
             DM_VW_region AS r ON w.City = r.City INNER JOIN
             DM_AutoHome_Map AS m ON m.province = r.Province
             GROUP BY w.Brand, m.province
             ORDER BY no desc'''
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
a,b=getCarOwner(u'凯美瑞')

def getColumnChart_p1():
    sql = """SELECT w.brand,r.Region,count(w.brand) as no
                 FROM BDCI.dbo.DW_AutoHome_WOM AS w INNER JOIN
                 BDCI.dbo.DM_VW_region AS r ON w.City = r.City
                 group by w.brand,r.Region
                 order by w.brand
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
            print(result[i_list])
            result[i_list][i_] = float('%.3f'% result[i_list][i_])
    return result
# getColumnChart_p1()

def getLevel1Attributes(paraList):
    newList = paraList.strip('[]').replace('"','').split(',')
    conn = pymssql.connect(server, user, password, "BDCI")
    sql = """SELECT avg(score) as Score
             ,Aspect
             ,Brand
             FROM DW_indexevaluationunpivot
             group by Brand,aspect
             order by Aspect asc
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
            print(result[i_list])
            result[i_list][i_] = float('%.2f'% result[i_list][i_])
    return result
# getLevel1Attributes("凯美瑞,帕萨特,雅阁,迈锐宝,迈锐宝XL,迈腾,蒙迪欧,名图")

def getLevel2Attributes(paraList):
    list1 = paraList.strip('[]')
    list2 = list1.replace('"','')
    list3 = list2.split(',')
    conn = pymssql.connect(server, user, password, "BDCI")
    sql = """SELECT  Brand
             ,Dimension
             ,keyindex
             ,KeyModifier
             ,SentenceAttitude
             ,case when SentenceAttitude >= 1 then '1'
             when SentenceAttitude = 0 then '0'
             when SentenceAttitude <= -1 then '-1' end  as Attitude
             ,frequency
             FROM DM_AutoHome_WOM_SecondLevelIndex_Noun_Modifier_Attitude_Frequency
             WHERE updateflag=0 
             """
    df = pd.read_sql_query(sql, conn)
    #brand = u'帕萨特'
    #dimension = u'操控'
    brand = list3[0]
    dimension = list3[1]
    df = df.loc[df['Brand']== brand]
    df = df.loc[df['Dimension']== dimension]
    indexList = df['keyindex'].tolist()
    indexList = list(set(indexList))
    result = []
    title = ['index','满意','没感觉','不满意']
    result.append(title)
    for index in indexList:
        manyiCount = 0
        meiganjueCount = 0
        bumanyiCount = 0
        attitudeList = df.loc[df['keyindex'] == index]['Attitude'].tolist()
        for attitude in attitudeList:
            if attitude == '1':
                manyiCount+=1
            elif attitude == '0':
                meiganjueCount+=1
            else:
                bumanyiCount+=1
        subResult = [index,manyiCount,meiganjueCount,bumanyiCount]
        result.append(subResult)
    return result[:10]
getLevel2Attributes("凯美瑞,空间")

def getPurpose(para):
    sql = """select *
             from DM_AutoHoome_Purpose
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
            print(result[i_list])
            result[i_list][i_] = float('%.3f'% result[i_list][i_])
    return result
# getPurpose('凯美瑞')
