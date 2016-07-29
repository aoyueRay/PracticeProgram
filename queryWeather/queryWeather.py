#-*- coding:utf-8 -*-

import urllib2
from StringIO import StringIO
import gzip
import json

class queryWeather():

    city_dict = {}

    url_head = 'http://wthrcdn.etouch.cn/weather_mini?citykey='
    # url_head = 'http://wthrcdn.etouch.cn/WeatherApi?citykey='

    # 读取城市代码文件，将城市名与城市代码格式化为字典形式
    def readFile(self):
        code_list = []    # 初始化一个城市代码列表
        city_list = []    # 初始化一个城市名称列表
        with open('CityCode.txt','rb') as f:
            infos = f.readlines()
        for each_info in infos:
            city_info = each_info.split('|')
            code_list.append(city_info[1])
            city_list.append(city_info[2])
        self.city_dict = dict(zip(city_list,code_list))
        return self.city_dict

    # 根据输入的城市名查询城市代码
    def queryCode(self,cityname):
        code = self.city_dict.get(cityname)
        return code

    # 根据城市代码查询天气信息
    def getWeatherInfos(self,citycode):
        url = self.url_head + citycode
        # print(url)

        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0')
        resp = urllib2.urlopen(req)

        # 判断信息是否经过gzip转码
        if resp.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(resp.read())
            f = gzip.GzipFile(fileobj=buf)
            weather_info = f.read()
        else:
            weather_info = resp.read()
        return weather_info

    # 将查询到的数据转换为json格式
    def loadJson(self,infos):
        data = json.loads(infos)
        return data

    # 将获取到的信息格式化输出
    def showInfos(self,data):
        if data['status'] == 1000:    # 查询返回结果正常
            print('★★★★' * 20)
            print('城市    ：%s ' % data['data']['city'].encode('utf-8'))
            print('当前温度：%s℃ ' % data['data']['wendu'].encode('utf-8'))
            print('感冒预防：%s' % data['data']['ganmao'].encode('utf-8'))
            if data['data'].get('aqi'):
                print('空气质量指数：%s' % data['data'].get('aqi').encode('utf-8'))
            else:
                print('空气质量指数：%s' % data['data'].get('aqi'))

            print('天气预报：')
            for i in range(5):
                print('\t%s：' % data['data']['forecast'][i]['date'].encode('utf-8'))
                print('\t\t最高温度:%s' %data['data']['forecast'][i]['high'].encode('utf-8'))
                print('\t\t最低温度:%s' %data['data']['forecast'][i]['low'].encode('utf-8'))
                print('\t\t天气    :%s' %data['data']['forecast'][i]['type'].encode('utf-8'))
                print('\t\t风向    :%s' %data['data']['forecast'][i]['fengxiang'].encode('utf-8'))
                print('\t\t风力    :%s' %data['data']['forecast'][i]['fengli'].encode('utf-8'))
                print('----' * 20)
            print('昨日温度：')
            print('\t%s：' % data['data']['yesterday']['date'].encode('utf-8'))
            print('\t\t最高温度:%s' % data['data']['yesterday']['high'].encode('utf-8'))
            print('\t\t最低温度:%s' % data['data']['yesterday']['low'].encode('utf-8'))
            print('\t\t天气    :%s' % data['data']['yesterday']['type'].encode('utf-8'))
            print('\t\t风向    :%s' % data['data']['yesterday']['fx'].encode('utf-8'))
            print('\t\t风力    :%s' % data['data']['yesterday']['fl'].encode('utf-8'))
            print('★★★★' * 20)
        else:    # 查询结果返回异常
            print('查询不到相关城市的天气资料。。。')


    # 功能页面
    def UI(self):
        print('**' * 40)
        print('\t\t\t天气预报查询\t\t\t')
        print('**' * 40)
        print('\t1)天气查询')
        print('\tq)退出')
        print('**' * 40)
        func_code = raw_input('请输入所需功能：')
        return func_code


if __name__ == "__main__":

    qw = queryWeather()
    qw.readFile()     # 获取代码列表
    while True:
        func_code = qw.UI()  # 获取用户输入的功能码
        if func_code == '1':
            cityname = raw_input('请输入需要查询的城市：')
            citycode = qw.queryCode(cityname)  # 获取城市对应的代码
            if not citycode:
                print("输入的城市名称有误！")
            else:
                weather_info = qw.getWeatherInfos(citycode)
                data = qw.loadJson(weather_info)
                qw.showInfos(data)
        elif func_code == 'q':
            break
        else:
            print('输入的功能不存在，请重新输入！')
    print('查询结束。。。')
