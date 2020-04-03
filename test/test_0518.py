from amazon.api import AmazonAPI


def amazon_api(country):
    if country=='us':
        amazon = AmazonAPI('AKIAJ2TPWCFJMKXPSJVQ','ixmfea5B2xKFukyuR/aiBzkI6f+umvISvYlzzBBy','newer027-20')
    elif country == 'ca':
        amazon = AmazonAPI('AKIAI3TBTKER2RZTHNNQ','9ahA2sNNnzcmDMuxnzLQUrDFKDzLuwuUREEFA3LX','newer02703-20',region='CA')
    elif country == 'fr':
        amazon = AmazonAPI('AKIAJ2TPWCFJMKXPSJVQ','ixmfea5B2xKFukyuR/aiBzkI6f+umvISvYlzzBBy','chengjiante0c-21',region='FR')
    elif country == 'de':
        amazon = AmazonAPI('AKIAI3TBTKER2RZTHNNQ','9ahA2sNNnzcmDMuxnzLQUrDFKDzLuwuUREEFA3LX','chengjiante06-21',region='DE')
    elif country == 'it':
        amazon = AmazonAPI('AKIAI3TBTKER2RZTHNNQ','9ahA2sNNnzcmDMuxnzLQUrDFKDzLuwuUREEFA3LX','chengjiant076-21',region='IT')
    elif country == 'jp':
        amazon = AmazonAPI('AKIAJ2TPWCFJMKXPSJVQ','ixmfea5B2xKFukyuR/aiBzkI6f+umvISvYlzzBBy','newer027-22',region="JP")
    elif country == 'es':
        amazon = AmazonAPI('AKIAI3TBTKER2RZTHNNQ','9ahA2sNNnzcmDMuxnzLQUrDFKDzLuwuUREEFA3LX','chengjiant04a-21',region='ES')
    else:
        amazon = AmazonAPI('AKIAI3TBTKER2RZTHNNQ','9ahA2sNNnzcmDMuxnzLQUrDFKDzLuwuUREEFA3LX','chengjiante00-21',region='UK')
    return amazon


amazon = amazon_api('fr')
product = amazon.lookup(ItemId='B01F6Z6BS8')
print(product.ean)


#amazon = AmazonAPI('AKIAI3TBTKER2RZTHNNQ','9ahA2sNNnzcmDMuxnzLQUrDFKDzLuwuUREEFA3LX','chengjiante0c-21',region='FR')