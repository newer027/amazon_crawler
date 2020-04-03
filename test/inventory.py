from amazon.api import AmazonAPI

amazon = AmazonAPI('AKIAJ2TPWCFJMKXPSJVQ','ixmfea5B2xKFukyuR/aiBzkI6f+umvISvYlzzBBy','newer027-20')

def build_cart_object(amazon,ItemId):
    product = amazon.lookup(ItemId=ItemId)
    return amazon.cart_create(
        {
            'offer_id': product.offer_id,
            'quantity': 1
        }
    )

def inventory_query(amazon,ItemId):
    info = {}
    cart = build_cart_object(amazon,ItemId)
    product = amazon.lookup(ItemId=ItemId)
    info['title'] = product.title
    item = {
        'offer_id': product._safe_get_element(
            'Offers.Offer.OfferListing.OfferListingId'),
        'quantity':999
    }
    amazon.cart_clear(cart.cart_id, cart.hmac)
    new_cart = amazon.cart_add(item, cart.cart_id, cart.hmac)
    for item in new_cart:
        cart_item_id = item.cart_item_id
    info['quantity'] = new_cart[cart_item_id].quantity
    return info

print(inventory_query(amazon,'B01N7MT107'))