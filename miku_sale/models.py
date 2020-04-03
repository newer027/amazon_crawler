import requests,json
import time
from lxml.html import fromstring


agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
headers = {
    'User-Agent': agent,
    'Host': "amazon.malllib.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Connection": "keep-alive"
}
s = requests.Session()
for category in list(range(3,37)):
    for rank in list(range(0,100)):
        data={'rank':rank+1,'categoryid':category+1,'country':1}
        page = s.post('http://amazon.malllib.com/amazon/home/get_bsrranksales.jhtml',data=data,headers=headers)
        print(json.loads(page.content))
        time.sleep(3)
