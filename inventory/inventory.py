from celery import Celery
from inventory.models import Inventory,Inventory_time
from celery.exceptions import SoftTimeLimitExceeded
from celery.utils.log import get_task_logger
from amazon.api import CartException
import re,pytz,datetime,time,random
from scrapy.selector import Selector
from core.amazon_api import amazon_api,pro_chi,s,pro_chi,USER_AGENTS,country_url
from amazon.api import AsinNotFound
from core.amazon_api import get_url


logger = get_task_logger(__name__)
app = Celery()
app.config_from_object('django.conf:settings')


@app.task(bind=True,time_limit=200,acks_late=True)
def inventory_query(self,ItemId,country,crontab=False):
    try:
        count=0
        while count<5:
            try:
                count+=1
                amazon = amazon_api(country)
                product = amazon.lookup(ItemId=ItemId)
                break
            except AsinNotFound:
                product = None
            except:
                time.sleep(0.1+random.random()*0.3)
                continue

        if crontab:
            inventory=Inventory.objects.filter(asin=ItemId,country=country)[0]
            if not product:
                inventory_time=Inventory_time(asin=inventory,inventory=0,sale_quan=0,
                                      bsr_rank=0,date=datetime.datetime.now(),price=0,
                                      sale_amount=0,star='ASIN已经下架')
                inventory_time.save()
                return "No_Asin"

        else:
            if not product:
                inventory=Inventory(title="No_Asin",asin=ItemId,country=country,inventory=0)
                inventory.save()
                return "No_Asin"
            else:
                print(product.title)
                inventory=Inventory(title=product.title,asin=ItemId,country=country)
                inventory.save()
        item = {
            'offer_id': product._safe_get_element(
                'Offers.Offer.OfferListing.OfferListingId'),
                'quantity':999}

        print('cart_create')
        count=0
        while count<5:
            try:
                count+=1
                product = amazon.lookup(ItemId=ItemId)
                cart = amazon.cart_create(
                    {
                    'offer_id': product.offer_id,
                    'quantity': 1
                    }
                )
                break
            except:
                time.sleep(0.1+random.random()*0.3)
                continue
        print('cart_clear')

        count=0
        while count<5:
            try:
                count+=1
                amazon.cart_clear(cart.cart_id, cart.hmac)
                break
            except:
                time.sleep(0.1+random.random()*0.3)
                continue

        print('cart_add')

        count=0
        while count<5:
            try:
                count+=1
                new_cart = amazon.cart_add(item, cart.cart_id, cart.hmac)
                break
            except:
                time.sleep(0.1+random.random()*0.3)
                continue

        try:
            for item in new_cart:
                cart_item_id = item.cart_item_id
            quantity = new_cart[cart_item_id].quantity
        except:
            if crontab and Inventory_time.objects.filter(asin=inventory)[1]:
                quantity=Inventory_time.objects.filter(asin=inventory)[0].inventory
            else:
                quantity=0

        #reviews_page=s.get(product.reviews[1],proxies=pro_chi())
        #if reviews_page.status_code != 200:
        #    print(reviews_page.status_code)
        #    raise Exception
        #else:
        #try:
            #reviews=int(re.sub(',','',Selector(text=reviews_page.content).xpath('/html/body/div[1]/div[2]/div[2]/div[1]/b').extract()[0].split(" ")[0][3:]))
        #except:
            #reviews=0
            #reviews_add=0
            #if crontab:
            #    reviews_add=reviews-Inventory_time.objects.filter(asin=inventory).first().reviews
        bsr_rank=product.sales_rank
        price=product.price_and_currency[0]
        price_unit=product.price_and_currency[1]
        sale_amount,sale_quan=0,0
        if inventory.inventory:
            sale_quan=inventory.inventory-int(quantity)
            if price:
                sale_amount=price*sale_quan
            else:
                sale_amount,price=0,0
            if sale_quan<0:
                sale_amount,sale_quan=0,0


        inventory_time=Inventory_time(asin=inventory,inventory=quantity,sale_quan=sale_quan,
                                      bsr_rank=bsr_rank,date=datetime.datetime.now(),price=price,
                                      sale_amount=sale_amount)
        inventory_time.save()
        inventory.inventory=quantity
        #if not crontab:
        inventory.img_url=product.medium_image_url
        inventory.detail_page_url=product.detail_page_url
        inventory.category=product.product_group
        inventory.price_unit=price_unit
        inventory.save()
        get_reviews.delay(country,inventory.asin,crontab)
            #except:
        #    inventory.inventory = 0
        #    inventory.save()
    except CartException:
        logger.info("ASIN商品不存在")
    except SoftTimeLimitExceeded:
        logger.info("Soft Time Limit Exceeded")
    except Exception as e:
        if crontab:
            dt = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=20)
            self.retry(eta=dt, exc=e, max_retries=1)



@app.task(bind=True,time_limit=200,acks_late=True,default_retry_delay=30,max_retries=3)
def get_reviews(self,country,asin,crontab):

    reviews_page=get_url('product-reviews/'+asin+'/ref=cm_cr_arp_d_viewopt_srt?sortBy=recent&pageNumber=1',country)
    if country in ['de','uk','fr','it','es']:
        star=(Selector(text=reviews_page.content).xpath('.//*[@id="cm_cr-product_info"]/div/div[1]/div[3]/span/text()').extract()[0]).split(" ")[0]
    elif country=='jp':
        star=(Selector(text=reviews_page.content).xpath('.//*[@id="cm_cr-product_info"]/div/div[1]/div[3]/span/text()').extract()[0])[-3:]
    else:
        star=(Selector(text=reviews_page.content).xpath('.//*[@id="cm_cr-product_info"]/div/div[1]/div[3]/span/a/span/text()').extract()[0]).split(" ")[0]
    reviews=Selector(text=reviews_page.content).xpath('.//*[@id="cm_cr-product_info"]/div/div[1]/div[2]/div/div/div[2]/div/span/text()').extract()[0]
    reviews=int(re.sub(",","",reviews))

    inventory=Inventory.objects.filter(asin=asin)[0]
    inventory_time=Inventory_time.objects.filter(asin=inventory)[0]
    if reviews_page:
        inventory_time.reviews=reviews
        inventory_time.star=star
        if crontab:
            try:
                old_reviews=Inventory_time.objects.filter(asin=inventory)[1].reviews
            except:
                old_reviews=0
            reviews_add=reviews-old_reviews
            if reviews_add>=0:
                inventory_time.reviews_add=reviews_add
    if crontab and not reviews_page:
        inventory_time.reviews=Inventory_time.objects.filter(asin=inventory)[1].reviews
        inventory_time.star=Inventory_time.objects.filter(asin=inventory)[1].star
    inventory_time.save()


"""

from inventory.models import Inventory_time,Inventory
for in_ti in Inventory_time.objects.all():
    if in_ti.sale_amount==0:
        try:
            in_ti.sale_amount=in_ti.price*in_ti.sale_quan
            in_ti.save()
        except:
            pass


from inventory.models import Inventory_time,Inventory
for inventory in Inventory.objects.all():
    try:
        inventory_time= Inventory_time.objects.filter(asin=inventory)[0]
        inventory_time.sale_quan=Inventory_time.objects.filter(asin=inventory)[1].inventory-inventory_time.inventory
        inventory_time.save()
    except:
        pass
"""