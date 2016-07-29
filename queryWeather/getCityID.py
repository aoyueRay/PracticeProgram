#-*- coding:utf-8 -*-

import urllib2
from lxml import etree

class getCode():
    url = 'http://www.cnblogs.com/geovindu/articles/3769024.html'

    # 通过url获取当前url的html源代码
    def getHtml(self,url):
        req = urllib2.Request(url)    # request
        resp = urllib2.urlopen(req)    # response
        html = resp.read()    # html
        return html

    # 将信息写入文件中
    def writeFile(self,infos):
        with open('CityCode.txt','ab') as f:
            f.write(infos)
            f.write('\n')

    # 通过html源代码，利用xpath获取城市信息
    def getInfos(self,html):
        tree = etree.HTML(html)
        tr = tree.xpath('//tbody/tr') # 定位到表格的每一行
        for each_id in range(1,len(tr)):
            infos = tr[each_id].xpath('td')
            city_infos = ''
            for each_info in infos:
                city_infos = city_infos + each_info.text + '|'
            # print(city_infos)
            self.writeFile(city_infos.encode('utf-8'))

if __name__ == '__main__':
    url = 'http://www.cnblogs.com/geovindu/articles/3769024.html'
    getid = getCode()
    html = getid.getHtml(url)
    getid.getInfos(html)




