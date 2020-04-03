import time, requests
from selenium import webdriver
from validation import validation
from PIL import Image
from pytesseract import image_to_string
from random import *
from urllib.request import urlretrieve
from amazon.api import AmazonAPI


def validate(driver):
    im = driver.find_element_by_id('auth-captcha-image')
    im = im.get_attribute('src')
    #urlretrieve(im, "captcha.jpg")
    f = open('captcha.jpg','wb')
    f.write(requests.get(im).content)
    f.close()
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


amazon = AmazonAPI('AKIAJ2TPWCFJMKXPSJVQ','ixmfea5B2xKFukyuR/aiBzkI6f+umvISvYlzzBBy','newer027-20')
asin="B01LCDJ7LG"
product = amazon.lookup(ItemId=asin)
ean = product.ean
print(product)
product_url = "https://vendorexpress.amazon.com/supplyProductDetails?asin=" + asin + "&hasRetailOffer=false&externalIdType=EAN&externalId=" + ean + "&isDfEligible=true&isPoEligible=true&productType="


"""
driver = webdriver.Chrome("/Users/Jacob/Desktop/amazon_keyword/chromedriver")
driver.get(product_url)
search_box = driver.find_element_by_id('ap_email')
search_box.send_keys(validation['id'])
while True:
    validate(driver)
    time.sleep(5)
    if driver.current_url == product_url:
        break
keyword = driver.find_element_by_id("searchTerms").get_attribute('value')
print ('{0}: {1}'.format(asin, keyword))


#list = driver.find_elements(By.XPATH, '//div[@class=\'a-radio eligibility-check-radio\'][2]')
#for item in list:
#    item.click()


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import requests

driver.find_element(By.XPATH, "//*[@id='isMultiPackage']/fieldset/span/div[2]/label/input").click()
driver.find_element(By.XPATH, "//*[@id='hasShortShelfLife']/fieldset/span/div[2]/label/input").click()
driver.find_element(By.XPATH, "//*[@id='isHazmat']/fieldset/span/div[2]/label/input").click()
#driver.find_elements_by_name("isMultiPackage")[1].click()
#driver.find_elements_by_name("hasShortShelfLife")[1].click()
#driver.find_elements_by_name("isHazmat")[1].click()
driver.find_element(By.XPATH, "//*[@id='isDirectFulfillment']/fieldset/span/ul/li[1]/span/div/div/div/div/label/input").click()
#driver.find_elements_by_name("isDirectFulfillment")[0].click()
driver.find_element_by_id("check-eligibility-button-announce").click()
wait = WebDriverWait(driver, 120)
msrp = driver.find_element_by_id('msrp')
msrp.send_keys(9999)
unitCost = driver.find_element_by_id('unitCost')
unitCost.send_keys(55)
driver.find_element_by_name('shouldDisplayMsrp').click()
driver.find_element_by_id("check-unit-cost-button-announce").click()
try:
    change_cost = driver.find_element_by_id("accept-proposed-cost-preferred-radio")
    change_cost.click()
    driver.find_element_by_id("check-unit-cost-button-announce").click()
finally:
    keyword = driver.find_element_by_id("searchTerms")
    keyword = keyword.get_attribute('value')
    print ('{0}: {1}'.format(product['name'], keyword))

"""


"""
dorpdown = driver.find_element_by_id('a-popover-2')
dorpdown.click()
dorpdown.send_keys(Keys.DOWN)
dorpdown.send_keys(Keys.RETURN)
ean = driver.find_element_by_id('externalId')
ean.clear()
ean.send_keys(Keys.COMMAND, 'v')
driver.find_element_by_class_name('a-button-input').click()
"""

print("done")



#driver.find_element_by_name('Output')
#time.sleep(3) # Let the user actually see something!
#driver.quit()
#window_handles
#html = driver.page_source
#soup = BeautifulSoup(html, "lxml")
#print(soup)

#html = driver.page_source
#soup = BeautifulSoup(html, "lxml")
#f = open('workfile', 'w')
#f.write(html)
#wait = WebDriverWait(browser, 10)
"""
try:
    element = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.ID, "ASIN-to-EAN_ItemId"))
    )
except:
    print("wait to long")


html = driver.page_source
keyword = 'class=\"a-size-large\"'
befor_keyowrd, keyword, after_keyword = html.partition(keyword)
print(len(befor_keyowrd),len(after_keyword))
keyword = 'id=\"expandTitleToggle\"'
befor_keyowrd, keyword, after_keyword = after_keyword.partition(keyword)
print(befor_keyowrd,len(after_keyword))
"""
#soup = BeautifulSoup(html, "lxml")
#print(soup.find_element_by_id("titleSection"))
#name = soup.title.string[0:len(soup.title.string)-4]
#print(name)

"""
ProductPageLink = driver.find_element_by_id('image')
ProductPageLink = ProductPageLink.find_elements_by_tag_name('a').get_attribute('href')
print(ProductPageLink)
driver = webdriver.Firefox()
driver.get(ProductPageLink)
product['name'] = driver.find_element_by_id('productTitle')
print(product)

ffprofile = webdriver.FirefoxProfile('/Users/Jacob/Library/Application Support/Firefox/Profiles/zyz9asye.default/')
print(ffprofile)
driver = webdriver.Firefox(firefox_profile=ffprofile)
driver = webdriver.Firefox()
driver = webdriver.Chrome('/Users/Jacob/Desktop/amazon_cralwer/amazon_crawler/test/chromedriver')

path = "https://vendorexpress.amazon.com/supplyProductDetails?asin=" + asin + "&hasRetailOffer=false&externalIdType=EAN&externalId=" + ean + "&isDfEligible=true&isPoEligible=true&productType="
page = requests.get(path,headers=headers)
tree = fromstring(page.content)
print(tree.findtext('//*[@id="after-pricing-section"]/div[10]'))
"""
