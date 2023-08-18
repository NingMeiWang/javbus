import requests, json, time, os, sys
sys.path.append('.')
requests.packages.urllib3.disable_warnings()
try:
    from pusher import pusher
except:
    pass
from lxml import etree


cookie='4fJN_2132_saltkey=ROLglA25; 4fJN_2132_lastvisit=1691911189; 4fJN_2132_sid=CXmmgr; 4fJN_2132__refer=%252Fforum%252Fhome.php%253Fmod%253Dspacecp%2526ac%253Dcredit; 4fJN_2132_sendmail=1; 4fJN_2132_seccodecSCXmmgr=13998.4618ebc78f4d2ae56a; 4fJN_2132_ulastactivity=6ab33u5QL777jG2Ee0y8kJS%2FdqrnAHs4zZNpcZhdrNArh1QSdqjn; 4fJN_2132_lastcheckfeed=412165%7C1691914820; 4fJN_2132_checkfollow=1; 4fJN_2132_lip=162.158.171.27%2C1691890076; 4fJN_2132_auth=505dPmWHcaaqEvr1bL%2FUWypCQFwgLl50HazBoNfgfwFmMfv6sA%2F0%2BxEDk4dVSKUVq3ygCjLzGVfMsBWkr30RUAh3qDE; bus_auth=214dKXG1s40muOq9s2nDsb7JHXQeVrtJk%2BgECXKdlciNtr%2F0xUKDfo1YNGanXXh5; 4fJN_2132_nofavfid=1; 4fJN_2132_onlineusernum=9588; 4fJN_2132_checkpm=1; 4fJN_2132_lastact=1691914831%09home.php%09spacecp'


def run(*arg):
    msg = ""
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'})

    # 签到
    url = "https://www.javbus.com/forum/home.php?mod=spacecp&ac=credit"
    headers = {
        'authority': 'www.javbus.com',
        'method': 'GET',
        'path': '/forum/home.php?mod=spacecp&ac=credit',
        'scheme': 'https',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
        #'Connection' : 'keep-alive',
        #'Host' : 'www.right.com.cn',
        'Upgrade-Insecure-Requests' : '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language' : 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Cookie': cookie,
        'referer': 'https://www.javbus.com/forum/home.php?mod=spacecp'
    }
    try:
        r = s.get(url, headers=headers, timeout=120)
        # print(r.text)
        if '每天登录' in r.text:
            h = etree.HTML(r.text)
            data = h.xpath('//tr/td[6]/text()')
            msg += f'签到成功或今日已签到，最后签到时间：{data[0]}'
        else:
            msg += '签到失败，可能是cookie失效了！'
            pusher(msg)
    except:
        msg = '无法正常连接到网站，请尝试改变网络环境，试下本地能不能跑脚本，或者换几个时间点执行脚本'
    return msg + '\n'

def main(*arg):
    msg = ""
    global cookie
    if "\\n" in cookie:
        clist = cookie.split("\\n")
    else:
        clist = cookie.split("\n")
    i = 0
    while i < len(clist):
        msg += f"第 {i+1} 个账号开始执行任务\n"
        cookie = clist[i]
        msg += run(cookie)
        i += 1
    print(msg[:-1])
    return msg[:-1]


if __name__ == "__main__":
    if cookie:
        print("----------巴士论坛开始尝试签到----------")
        main()
        print("----------巴士论坛签到执行完毕----------")
