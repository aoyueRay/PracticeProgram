# -*- coding: utf-8 -*-
import urllib2
import json
import time


def get_html(url):
    send_headers = {
        'User-Agent':'"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0"',
        'Accept':'*/*',
        'Connection':'keep-alive',
        'Host':'xueqiu.com',
        'Referer':'https://xueqiu.com/p/discover',
        'X-Requested-With':'XMLHttpRequest',
        'Cookie':'"s=21xu11kcml; Hm_lvt_1db88642e346389874251b5a1eded6e3=1469173879,1469173909,1469176049,1469177558; bid=61c6b89734f54943a27abd7000d26c89_ip6h16c5; xq_a_token=57bf652c0e6df244fd30412ca02712e4887c9350; xq_r_token=d1e748e7a58554e2c8dcde4d7e0b0496b16179b7; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1469177558; xqat=57bf652c0e6df244fd30412ca02712e4887c9350; xq_is_login=1; u=1796886594; xq_token_expire=Tue%20Aug%2016%202016%2015%3A22%3A47%20GMT%2B0800%20(CST); snbim_minify=true; webp=0"',  # 这里需替换cookie值，否则会请求失败
    }
    req = urllib2.Request(url, headers=send_headers)
    resp = urllib2.urlopen(req)
    html = resp.read()
    return html


def fetch_portfolio(code):
    url = 'http://xueqiu.com/p/' + code
    html = get_html(url)
    # 直接用字符匹配找出位置，然后截取字符
    pos_start = html.find('SNB.cubeInfo = ') + 15
    pos_end = html.find('SNB.cubePieData')
    data = html[pos_start:pos_end]
    dic = json.loads(data)

    print '收益率', dic['total_gain']
    stocks = dic['view_rebalancing']['holdings']
    for s in stocks:
        print s['stock_name'], s['weight']


def get_portfolio_list(page):
    url = 'https://xueqiu.com/cubes/discover/rank/cube/list.json?category=10&count=10&market=cn&page=%d' % page
    print(url)
    html = get_html(url)
    print(html)
    dic = json.loads(html)
    for p in dic['list']:
        print p['symbol'], p['name']
        # 结果存储添加至全局变量中
        portfolio_list.append((p['symbol'], p['name']))


# 抓取组合列表
global portfolio_list
portfolio_list = []
for page in xrange(1, 3):  # 需要抓取更多页，修改这里的page上限
    print 'fetch page', page
    get_portfolio_list(page)
    time.sleep(2)
# print portfolio_list
print '============================'

# 抓取每个组合的详细信息
for p in portfolio_list:
    print 'fetch', p[0], p[1]
    fetch_portfolio(p[0])
    time.sleep(1)
    print '---------------------------'
