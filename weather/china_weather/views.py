from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse,render,redirect
import pandas as pd
import numpy as np
from django.utils.safestring import mark_safe
from sqlalchemy import create_engine,text
import json

#创建mysql的连接
engine=create_engine('mysql+pymysql://root:root@192.168.56.101:3306/china_all')
table_name=['china_map','province_temp','province_pressure','city_temp','city_precipitation_top10']
sql_base='select * from '

def convert_numpy_types(obj):
    """递归转换numpy类型为Python原生类型，以便JSON序列化"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {str(k) if isinstance(k, (np.integer, np.floating)) else k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_numpy_types(item) for item in obj)
    else:
        return obj

def load_data():
    """加载所有数据，在视图函数中调用"""
    try:
        #读取地图数据
        sql=text(sql_base+table_name[0])
        connect = engine.connect()
        map_data=pd.read_sql(sql,connect)
        connect.close()
        # map_data=pd.read_csv('static/data/各省份每月平均气温和风速-地图.csv',encoding='utf-8',header=None)
        # map_data.columns=['month','province','temp','wind_speed']
        map_data['temp']=np.round(map_data['temp']/10,0)
        map_data['wind_speed']=np.round(map_data['wind_speed']/10,0)
        # print(map_data.head(40))
        months=map_data['month'].unique()
        #各省份气温数据
        map_data1=dict()
        map_data2=dict()
        for item in months:
            mydata=map_data[map_data['month']==item]
            # print(mydata.head(40))
            data_temp=[]
            data_wind=[]
            for i in mydata.index:
                dict_temp={}
                dict_temp['name']=str(mydata.loc[i,'province'])
                dict_temp['value'] = float(mydata.loc[i, 'temp'])
                data_temp.append(dict_temp)
                dict_wind = {}
                dict_wind['name']=str(mydata.loc[i,'province'])
                dict_wind['value'] = float(mydata.loc[i, 'wind_speed'])
                data_wind.append(dict_wind)
            map_data1[int(item)]=data_temp
            map_data2[int(item)]=data_wind
        print(map_data1)
        #读取折线图数据
        sql=text(sql_base+table_name[1])
        connect = engine.connect()
        temp_province_data=pd.read_sql(sql,connect)
        connect.close()
        # temp_province_data=pd.read_csv('static/data/各省份每月平均气温-折线图.csv',encoding='utf-8',header=None)
        # temp_province_data.columns=['province','month','temp','temp_forecast']
        temp_province_data['temp']=np.round(temp_province_data['temp']/10,0)
        temp_province_data['temp_forecast']=np.round(temp_province_data['temp_forecast'],0)
        # print(temp_province_data.head())
        provinces=list(temp_province_data['province'].unique())
        line_data={}
        for item in provinces:
            temp_dict={}
            temp_province=temp_province_data[temp_province_data['province']==item]
            temp_dict['month']=[int(x) for x in temp_province['month'].values]
            temp_dict['temp'] = [float(x) for x in temp_province['temp'].values]
            temp_dict['temp_forecast'] = [float(x) for x in temp_province['temp_forecast'].values]
            line_data[str(item)]=temp_dict
        # print(line_data)
        #读取树图数据
        sql=text(sql_base+table_name[2])
        connect = engine.connect()
        pressure_data=pd.read_sql(sql,connect)
        connect.close()
        # pressure_data=pd.read_csv('static/data/各省份每月平均气压-矩形树图.csv',encoding='utf-8',header=None)
        # pressure_data.columns=['month','province','pressure']
        pressure_data['pressure']=pressure_data['pressure']/10
        # print(pressure_data.head())
        tree_data=dict()
        for item in months:
            mydata=pressure_data[pressure_data['month']==item]
            pressure_month=[]
            for i in mydata.index:
                pressure=dict()
                pressure['name']=str(mydata.loc[i,'province'])
                pressure['value'] = float(mydata.loc[i, 'pressure'])
                pressure_month.append(pressure)
            tree_data[int(item)]=pressure_month
        print(tree_data)


        #读取词云数据
        sql=text(sql_base+table_name[3])
        connect = engine.connect()
        city_temp_data=pd.read_sql(sql,connect)
        connect.close()
        city_temp_data['temp']=city_temp_data['temp']/10
        city_temp_data=city_temp_data.dropna()

        word_data=dict()
        for item in months:
            mydata=city_temp_data[city_temp_data['month']==item]
            temp_month=[]
            for i in mydata.index:
                temperature=dict()
                temperature['name']=str(mydata.loc[i,'city'])
                temperature['value'] = float(mydata.loc[i, 'temp'])
                temp_month.append(temperature)
            word_data[int(item)]=temp_month
        # print(word_data)

        #读取条形图数据
        sql=text(sql_base+table_name[4])
        connect = engine.connect()
        precipitation_data=pd.read_sql(sql,connect)
        connect.close()
        # precipitation_data=pd.read_csv('static/data/城市每月平均降水top10-条形图.csv',encoding='utf-8',header=None)
        # precipitation_data.columns=['month','city','precipitation_6']
        precipitation_data['precipitation_6']=precipitation_data['precipitation_6']/10
        # print(precipitation_data.head())
        bar_data=dict()
        for item in months:
            mydata=precipitation_data[precipitation_data['month']==item]
            # mydata=mydata.sort_values('precipitation_6')
            precipitation_month={}
            precipitation_month['city'] = [str(x) for x in mydata['city'].values]
            precipitation_month['precipitation'] = [float(x) for x in mydata['precipitation_6'].values]
            bar_data[int(item)] = precipitation_month
        # print(bar_data)
        
        # 转换所有numpy类型为Python原生类型
        result = {
            'map_data1': convert_numpy_types(map_data1),
            'map_data2': convert_numpy_types(map_data2),
            'provinces': [str(p) for p in provinces],
            'line_data': convert_numpy_types(line_data),
            'tree_data': convert_numpy_types(tree_data),
            'word_data': convert_numpy_types(word_data),
            'bar_data': convert_numpy_types(bar_data),
        }
        return result
    except Exception as e:
        print(f"数据库连接错误: {e}")
        # 如果数据库连接失败，返回空数据
        return {
            'map_data1': {},
            'map_data2': {},
            'provinces': [],
            'line_data': {},
            'tree_data': {},
            'word_data': {},
            'bar_data': {},
        }

def login(request):
    data = load_data()
    return render(request,'index.html',
                  {'map_data1':mark_safe(json.dumps(data['map_data1'], ensure_ascii=False)),
                   'map_data2': mark_safe(json.dumps(data['map_data2'], ensure_ascii=False)),
                   'provinces': mark_safe(json.dumps(data['provinces'], ensure_ascii=False)),
                   'line_data':mark_safe(json.dumps(data['line_data'], ensure_ascii=False)),
                   'tree_data': mark_safe(json.dumps(data['tree_data'], ensure_ascii=False)),
                   'word_data': mark_safe(json.dumps(data['word_data'], ensure_ascii=False)),
                   'bar_data': mark_safe(json.dumps(data['bar_data'], ensure_ascii=False)),
                  })

