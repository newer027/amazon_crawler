from amazon.api import AmazonAPI



""""
def build_cart_object():
    product = amazon.lookup(ItemId="B06Y1JY6WY")
    return amazon.cart_create(
        {
            'offer_id': product.offer_id,
            'quantity': 1
        }
    )

def cart_add():
    cart = build_cart_object(ItemId)
    product = amazon.lookup(ItemId=ItemId)
    item = {
        'offer_id': product._safe_get_element(
            'Offers.Offer.OfferListing.OfferListingId'),
        'quantity':999
    }
    amazon.cart_clear(cart.cart_id, cart.hmac)
    new_cart = amazon.cart_add(item, cart.cart_id, cart.hmac)
    for item in new_cart:
        cart_item_id = item.cart_item_id
    print(new_cart[cart_item_id].quantity)
"""


def test_search_n():
    """Test Product Search N.
    Tests that a product search n is working by testing that N results are
    returned.
    """
    products = amazon.search_n(
        30,
        Keywords='kindle',
        SearchIndex='All'
    )
    print(len(products))


def test_search_iterate_pages(keywords,asin):
    products = amazon.search(Keywords=keywords,SearchIndex='All')
    rank_index = 0
    for product in products:
        rank_index += 1
        try:
            if product.asin == asin:
                print(product.title,"ranked",rank_index,"in page",products.current_page+1)
                break
        except:
            print("did not find")



amazon = AmazonAPI('AKIAJ2TPWCFJMKXPSJVQ','ixmfea5B2xKFukyuR/aiBzkI6f+umvISvYlzzBBy','newer027-20')
keywords = 'internet of things oreilly'
asin = '0596528264'
test_search_n()
test_search_iterate_pages(keywords,asin)