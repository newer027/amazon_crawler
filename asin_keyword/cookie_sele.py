import time, pickle
from selenium import webdriver
from asin_keyword.validation import *
from PIL import Image
from pytesseract import image_to_string
from random import *
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
import requests, shutil,json,re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import *
from core.amazon_api import pro_chi
from selenium.common.exceptions import NoSuchElementException


def get_captcha(driver, element, path):
    # now that we have the preliminary stuff out of the way time to get that image :D
    location = element.location
    size = element.size
    # saves screenshot of entire page
    driver.save_screenshot(path)

    # uses PIL library to open image in memory
    image = Image.open(path)
    #image.show()
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    print(left, top, right, bottom)
    # image = image.crop((left, top, right, bottom))  # defines crop points
    image = image.crop((left*2, top*2, right*2, bottom*2))  # defines crop points
    image.save(path, 'jpeg')  # saves new cropped image


def validate(driver,country,validation):
    cap=False
    try:
        im = driver.find_element_by_id('auth-captcha-image')
        im = im.get_attribute('src')
        # urlretrieve(im, "captcha.jpeg")
        #get_captcha(driver,im,"captcha.jpeg")

        agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 Firefox/52.0'
        headers = {
            'User-Agent': agent,
            'Host': "opfcaptcha-prod.s3.amazonaws.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive"
        }
        print(im)
        response = requests.get(im, stream=True, headers=headers)
        with open('captcha.jpeg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        im = 'captcha.jpeg'
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
        #binaryImage.show()
        characters = image_to_string(binaryImage,config='-psm 7')
        char_list = characters.split(' ')
        characters = ''.join(char_list)
        print(characters)
        search_box = driver.find_element_by_id('auth-captcha-guess')
        for i in characters:
            time.sleep(0.5-random()*0.2)
            search_box.send_keys(i)
        time.sleep(3)
        cap=True
    except NoSuchElementException:
        print('no captcha')
        pass
    finally:
        search_box = driver.find_element_by_id('ap_password')
        if country=='jp':
            for i in validation['password']:
                time.sleep(0.8-random()*0.5)
                search_box.send_keys(i)
        else:
            for i in validation['password']:
                time.sleep(0.8-random()*0.5)
                search_box.send_keys(i)
        time.sleep(4)
        driver.find_element_by_id('signInSubmit').click()
        return cap

# amazon = AmazonAPI('AKIAJ2TPWCFJMKXPSJVQ','ixmfea5B2xKFukyuR/aiBzkI6f+umvISvYlzzBBy','newer027-20')
# asin="B01LCDJ7LG"
# ean='0848061039726'
# product = amazon.lookup(ItemId=asin)
# ean = product.ean
# print(ean)


# driver = webdriver.Chrome("/Users/Jacob/Desktop/amazon_keyword/chromedriver")
def cookie_sele(country):

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
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': proxyMeta,
        'ftpProxy': proxyMeta,
        'sslProxy': proxyMeta,
        'noProxy':''})
    """

    display = Display(visible=0, size=(1920, 1080)).start()
    driver = webdriver.Firefox()
    product_url_am = "https://vendorexpress.amazon.com/home?ref=VE_LANDING"
    product_url_eu = "https://vendorexpress.amazon.eu/"
    product_url_jp = "https://vendorexpress.amazon.co.jp/home?ref=VE_LANDING"

    #driver = webdriver.Chrome("/Users/Jacob/Desktop/amazon_keyword/chromedriver")
    try:
        if country=='am':
            driver.get(product_url_am)
            cookies="cookies_am.pkl"
            validation=validation_am

        elif country=='uk':
            driver.get(product_url_eu)
            driver.find_element_by_xpath('//*[@id="sign-in-link"]').click()
            cookies="cookies_uk.pkl"
            validation=validation_uk

        elif country=='fr':
            driver.get(product_url_eu)
            driver.find_element_by_id('change-marketplace-dropdown').click()
            time.sleep(1)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="a-popover-1"]/div/div/ul/li[5]'))).click()
            time.sleep(8)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sign-in-link"]'))).click()

            cookies="cookies_fr.pkl"
            validation=validation_fr

        elif country=='it':
            driver.get(product_url_eu)
            driver.find_element_by_id('change-marketplace-dropdown').click()
            time.sleep(1)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="a-popover-1"]/div/div/ul/li[1]'))).click()
            time.sleep(8)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sign-in-link"]'))).click()

            cookies="cookies_it.pkl"
            validation=validation_it

        elif country=='es':
            driver.get(product_url_eu)
            driver.find_element_by_id('change-marketplace-dropdown').click()
            time.sleep(1)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="a-popover-1"]/div/div/ul/li[2]'))).click()
            time.sleep(8)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sign-in-link"]'))).click()

            cookies="cookies_es.pkl"
            validation=validation_es

        elif country=='de':
            driver.get(product_url_eu)
            driver.find_element_by_id('change-marketplace-dropdown').click()
            time.sleep(1)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="a-popover-1"]/div/div/ul/li[4]'))).click()
            time.sleep(8)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sign-in-link"]'))).click()

            cookies="cookies_de.pkl"
            validation=validation_de

        else:
            driver.get(product_url_jp)
            cookies="cookies_jp.pkl"
            validation=validation_jp

        myElem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'ap_email')))
        #driver.find_element_by_id('ap_email')
        myElem.send_keys(validation['id'])
        time.sleep(5)
        num=0
        try:
            while num < 5:
                num += 1
                validate(driver,country,validation)
                time.sleep(10)
        except:
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            print(soup.title.string)
            pickle.dump( driver.get_cookies() , open(cookies,"wb"))
    except:
        pass

    finally:
        driver.quit()
        display.stop()
