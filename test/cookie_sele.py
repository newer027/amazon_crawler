import time, pickle
from selenium import webdriver
from validation import validation
from PIL import Image
from pytesseract import image_to_string
from random import *
from urllib.request import urlretrieve
from bs4 import BeautifulSoup


def get_captcha(driver, element, path):
    # now that we have the preliminary stuff out of the way time to get that image :D
    location = element.location
    size = element.size
    # saves screenshot of entire page
    driver.save_screenshot(path)

    # uses PIL library to open image in memory
    image = Image.open(path)
    image.show()
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
    #im = im.get_attribute('src')
    #urlretrieve(im, "captcha.jpg")
    get_captcha(driver,im,"captcha.jpeg")

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
    binaryImage.show()
    characters = image_to_string(binaryImage,config='-psm 7')
    char_list = characters.split(' ')
    characters = ''.join(char_list)
    print(characters)
    search_box = driver.find_element_by_id('ap_password')
    for i in validation['password']:
        time.sleep(0.4-random()*0.1)
        search_box.send_keys(i)
    time.sleep(1)
    search_box = driver.find_element_by_id('auth-captcha-guess')
    for i in characters:
        time.sleep(0.3-random()*0.1)
        search_box.send_keys(i)
    time.sleep(2)
    driver.find_element_by_id('signInSubmit').click()


#amazon = AmazonAPI('AKIAJ2TPWCFJMKXPSJVQ','ixmfea5B2xKFukyuR/aiBzkI6f+umvISvYlzzBBy','newer027-20')
asin="B01LCDJ7LG"
ean='0848061039726'
#product = amazon.lookup(ItemId=asin)
#ean = product.ean
print(ean)
product_url = "https://vendorexpress.amazon.com/supplyProductDetails?asin=" + asin + "&hasRetailOffer=false&externalIdType=EAN&externalId=" + ean + "&isDfEligible=true&isPoEligible=true&productType="

#driver = webdriver.Chrome("/Users/Jacob/Desktop/amazon_keyword/chromedriver")
driver = webdriver.Firefox()
driver.get(product_url)
search_box = driver.find_element_by_id('ap_email')
search_box.send_keys(validation['id'])
validate(driver)
time.sleep(30)
html = driver.page_source
soup = BeautifulSoup(html, "lxml")
print(soup.find("input", {'id': "searchTerms"}).attrs['value'])
pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
