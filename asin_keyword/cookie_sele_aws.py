import time, pickle
from selenium import webdriver
from .validation import validation
from PIL import Image
from pytesseract import image_to_string
from random import *
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from .emails import send_feedback_email
from pyvirtualdisplay import Display
import requests, shutil


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
    #image = image.crop((left, top, right, bottom))  # defines crop points
    image = image.crop((left*2, top*2, right*2, bottom*2))  # defines crop points
    image.save(path, 'jpeg')  # saves new cropped image


def validate(driver):
    im = driver.find_element_by_id('auth-captcha-image')
    im = im.get_attribute('src')
    #urlretrieve(im, "captcha.jpeg")
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
    search_box = driver.find_element_by_id('ap_password')
    for i in validation['password']:
        time.sleep(0.8-random()*0.5)
        search_box.send_keys(i)
    time.sleep(4)
    search_box = driver.find_element_by_id('auth-captcha-guess')
    for i in characters:
        time.sleep(0.5-random()*0.2)
        search_box.send_keys(i)
    time.sleep(5)
    driver.find_element_by_id('signInSubmit').click()


#amazon = AmazonAPI('AKIAJ2TPWCFJMKXPSJVQ','ixmfea5B2xKFukyuR/aiBzkI6f+umvISvYlzzBBy','newer027-20')
#asin="B01LCDJ7LG"
#ean='0848061039726'
#product = amazon.lookup(ItemId=asin)
#ean = product.ean
#print(ean)
product_url_us = "https://vendorexpress.amazon.com/home?ref=VE_LANDING"
product_url_eu = "https://vendorexpress.amazon.eu/home?ref=VE_LANDING"

#driver = webdriver.Chrome("/Users/Jacob/Desktop/amazon_keyword/chromedriver")
def cookie_sele():
    display = Display(visible=0, size=(1920, 1080)).start()
    driver = webdriver.Firefox()
    #driver = webdriver.Chrome("/Users/Jacob/Desktop/amazon_keyword/chromedriver")
    try:
        driver.get(product_url_us)
        search_box = driver.find_element_by_id('ap_email')
        search_box.send_keys(validation['id'])
        time.sleep(5)
        while driver.current_url.startswith("https://vendorexpress.amazon.com/ap/signin"):
            validate(driver)
            time.sleep(30)
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        print(soup.title.string)
        pickle.dump( driver.get_cookies() , open("cookies_us.pkl","wb"))

        driver.get(product_url_eu)
        search_box = driver.find_element_by_id('ap_email')
        search_box.send_keys(validation['id'])
        time.sleep(5)
        while driver.current_url.startswith("https://vendorexpress.amazon.eu/ap/signin"):
            validate(driver)
            time.sleep(30)
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        print(soup.title.string)
        pickle.dump( driver.get_cookies() , open("cookies_eu.pkl","wb"))

        import paramiko
        source_us = '/home/ubuntu/myprojects/amazon_crawler/cookies_us.pkl'
        dest_us = '/home/ubuntu/myprojects/amazon_crawler/cookies_us.pkl'
        source_eu = '/home/ubuntu/myprojects/amazon_crawler/cookies_eu.pkl'
        dest_eu = '/home/ubuntu/myprojects/amazon_crawler/cookies_eu.pkl'
        hostname = '119.23.46.230'
        port = 22 # default port for SSH
        username = 'ubuntu'
        password = 'ML#$gbal'
        try:
            t = paramiko.Transport((hostname, port))
            t.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(t)
            sftp.put(source_us, dest_us)
            sftp.put(source_eu, dest_eu)
        finally:
            t.close()

        send_feedback_email('amz668@amz668.com','cookies saved!')
    finally:
        driver.quit()
