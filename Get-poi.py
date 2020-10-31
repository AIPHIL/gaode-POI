'''
利用高德地图api实现经纬度周边搜索并提取用地信息
'''

import requests
import pandas as pd
import time
import importlib
import sys
import numpy as np

importlib.reload(sys)
# sys.setdefaultencoding("utf-8")
start = time.clock()

# 读取csv经纬度数据
def parse():
    totalListData = pd.read_csv('locs.csv')
    datas = np.array(totalListData)
    return datas

# 坐标转换
def transform(location):
    parameters = {'coordsys': 'gps', 'locations': location, 'key': 'd672d1**************************'}
    base = 'http://restapi.amap.com/v3/assistant/coordinate/convert'
    response = requests.get(base, parameters)
    answer = response.json()
    an = answer['locations']
    return an

# 周边搜索
def around(location, distance):
    keywords = '购物服务|餐饮服务|商务住宅|生活服务|科教文化服务|住宿服务|体育休闲服务|风景名胜|交通设施服务|公司企业|' \
               '医疗保健服务|政府机构及社会团体'
    parameters = {'location': location, 'keywords': keywords,'key': 'd672d**************************'}', 'radius': distance}
    base = 'http://restapi.amap.com/v3/place/around'
    response = requests.get(base, parameters)
    answer = response.json()
    back = []
    test = answer['pois']  # 判断pois是否为空
    num = len(test)
    if test:
        for i in range(num):
            back0 = answer['pois'][i]['type']
            back.append(back0)
    else:
        distance = distance + 10
        back = around(location, distance)
    return back

if __name__ == '__main__':
    i = 0
    count = 0
    df = pd.DataFrame(columns=['location', 'surroundings_type'])
    # locations = parse(item)
    locations = parse()

    for locat in range(len(locations)):
        distance = 20   # 初始周边搜索半径m
        location = locations[locat]
        tf = transform(location)
        d_type = around(tf, distance)
        number = len(d_type)
        end_type = []
        limit = ['学校', '商场', '机场相关', '火车站']
        for t in range(number):  # 将list类型的end_type单个字符串元素分割
            split_type = d_type[t].split(";")
            k = 0
            for s in range(len(limit)):
                if split_type[1] == limit[s]:
                    end_type.append(split_type[1])
                    k = 1
            if k == 0:
                end_type.append(split_type[0])
            print("step:%s  type: %s" % (locat, split_type))
        str = " "
        end_type = str.join(list(set(end_type)))  # 将list类型的end_type元素去重复并去括、引号
        location = str.join(location)
        df.loc[i] = [location, end_type]
        i = i + 1
    df.to_csv('locdetail1-0.csv', index=False)
    end = time.clock()
    print(end-start)
