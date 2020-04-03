from bs4 import BeautifulSoup
from PIL import Image
from pytesseract import image_to_string
import requests, requests.utils, pickle
from lxml.html import fromstring
import bs4
try:
    import cookielib
except:
    import http.cookiejar as cookielib


r = requests.get('https://vendorexpress.amazon.com/home')


agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
headers = {
    'User-Agent': agent,
    'Host': "vendorexpress.amazon.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Connection": "keep-alive"
}


post_url = r.url




def get_captcha(session):
    html = session.get(post_url, headers=headers).text
    soup = BeautifulSoup(html, "lxml")
    print(soup.title)
    im = soup.find(id='auth-captcha-image')['src']
    print(im)
    f = open('captcha.jpg','wb')
    headers['Host'] = 'opfcaptcha-prod.s3.amazonaws.com'
    f.write(requests.get(im, headers=headers).content)
    f.close()
    #urlretrieve(im, "captcha.jpg")
    im = 'captcha.jpg'
    im = Image.open(im)
    im = im.convert('L')
    def initTable(threshold=140):
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                 table.append(1)
        return table
    binaryImage = im.point(initTable(), '1')
    binaryImage.show()
    characters = image_to_string(binaryImage,config='-psm 7')
    char_list = characters.split(' ')
    characters = ''.join(char_list)
    print(characters)
    return characters


def login_session(id, password):
    session = requests.session()
    url = 'https://vendorexpress.amazon.com'
    session.get(url, headers=headers)  # 访问首页产生 cookies
    headers['Referer'] = "https://vendorexpress.amazon.com/ap/signin"
    postdata = {
    'email': id,
    'create':0,
    'password': password,
    'use_image_captcha': 'true',
    'use_audio_captcha': 'false',
    'guess': get_captcha(session),
    'rememberMe': 'true',
    }
    response = session.post(post_url, data=postdata, headers=headers)

    soup = bs4.BeautifulSoup(response.text, "html.parser")
    warning = soup.find('div', {'id': 'message_warning'})
    if warning:
        print('Failed to login: {0}'.format(warning.text))

    page = session.get('https://vendorexpress.amazon.com/supplyProductDetails?asin=B01LCDJ7LG&hasRetailOffer=false&externalIdType=EAN&externalId=0848061039948&isDfEligible=true&isPoEligible=true&productType=',headers=headers)
    print(page.request.headers)
    tree = fromstring(page.content)
    print(tree.findtext('.//title'))
    return session