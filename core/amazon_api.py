from amazon.api import AmazonAPI
import random,requests
import time
from scrapy.selector import Selector
from .asso_id import amazon_id_1,amazon_id_2,amazon_id_3

ABOVE_V1 = ['v1','v2','v3']
ABOVE_V2 = ['v2','v3']
ABOVE_V3 = ['v3']


def amazon_api(country):
    if country in ['us','fr','it','jp']:
        number=int(time.time()*10) % 3
        amazon_id=(amazon_id_1,amazon_id_2,amazon_id_3)[number]
        return AmazonAPI(amazon_id['asso_id'],amazon_id['asso_key'],amazon_id[country],region=country.upper())
    elif country in ['ca','es']:
        number=int(time.time()*10) % 2
        amazon_id=(amazon_id_2,amazon_id_3)[number]
        return AmazonAPI(amazon_id['asso_id'],amazon_id['asso_key'],amazon_id[country],region=country.upper())
    else:
        return AmazonAPI(amazon_id_1['asso_id'],amazon_id_1['asso_key'],amazon_id_1[country],region=country.upper())
        #amazon_id=random.choice([amazon_id_2])


def amazon_api_test(country,second=0):
    if not second:
        return AmazonAPI(amazon_id_1['asso_id'],amazon_id_1['asso_key'],amazon_id_1[country],region=country.upper())
    elif second==1:
        return AmazonAPI(amazon_id_2['asso_id'],amazon_id_2['asso_key'],amazon_id_2[country],region=country.upper())
    else:
        return AmazonAPI(amazon_id_3['asso_id'],amazon_id_3['asso_key'],amazon_id_3[country],region=country.upper())


def country_url(country):
    if country=='us':
        url = 'https://www.amazon.com/'
    elif country == 'ca':
        url = 'https://www.amazon.ca/'
    elif country == 'fr':
        url = 'https://www.amazon.fr/'
    elif country == 'de':
        url = 'https://www.amazon.de/'
    elif country == 'it':
        url = 'https://www.amazon.it/'
    elif country == 'jp':
        url = 'https://www.amazon.co.jp/'
    elif country == 'es':
        url = 'https://www.amazon.es/'
    else:
        url = 'https://www.amazon.co.uk/'
    return url


def pro_chi():
    """
    pro_chi=requests.get('http://127.0.0.1:8000/?types=0&count=500&country=%E5%9B%BD%E5%86%85').text
    pro_chi = json.loads(pro_chi)
    pro=pro_chi[random.randrange(len(pro_chi))]
    #pro=(pro[0],str(pro[1]))
    proxyMeta0 = "http://%(host)s:%(port)s" % {
      "host" : pro[0],
      "port" : str(pro[1]),
    }
    """

    proxyHost = "proxy.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "H7MC0548HBREWI6D"
    proxyPass = "4027F911A17158D1"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }

    proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }
    #dayOfWeek = datetime.today().weekday()
    #if  not (dayOfWeek % 2):
    return proxies
    #else:
    #    return {'http': proxyMeta0}


USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

agent = random.choice(USER_AGENTS)
headers = {
    'User-Agent': agent,
    'Host': "www.amazon.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    #"Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Connection": "keep-alive"
}
s = requests.Session()

def get_url(url_add,country=None,host=None):

    url_start=''
    if country:
        url_start=country_url(country)
        headers['Host']=country_url(country).split("/")[2]
    if host:
        headers['Host']=host
    s = requests.Session()

    page=None
    count=0
    while count<8:
        try:
            count+=1
            proxy=pro_chi()
            page = s.get(url_start+url_add,headers=headers, proxies=proxy)
            if page.status_code==200 and page:
                return page
            check = s.get('http://proxies.site-digger.com/proxy-detect/',headers=headers,proxies=proxy)
            print(Selector(text=check.content).xpath('/html/body/p[3]').extract()[0])
        except:
            print("Connection refused by the server..")
            time.sleep(1+random.random()*2.5)
            print("Was a nice sleep, now let me continue...")
            continue
    return page