# -*- coding: utf-8 -*-

from celery import Celery
from core.amazon_api import get_url
import json


app = Celery()
app.config_from_object('django.conf:settings')

@app.task(bind=True,time_limit=30,acks_late=True,default_retry_delay=3, max_retries=3)
def get_rele_word(self,in_word,country):
    if country=='us':
        url_add='https://completion.amazon.com/search/complete?method=completion&search-alias=aps&client=amazon-search-ui&mkt=1&fb=1&sc=1&q='+in_word
        host='completion.amazon.com'
    elif country=='ca':
        url_add='https://completion.amazon.com/search/complete?method=completion&mkt=7&l=en_CA&client=amazon-search-ui&search-alias=aps&qs=&cf=1&fb=1&sc=1&q='+in_word
        host='completion.amazon.com'
    elif country=='fr':
        url_add='https://completion.amazon.co.uk/search/complete?method=completion&mkt=5&l=fr_FR&client=amazon-search-ui&search-alias=aps&qs=&cf=1&fb=1&sc=1&q='+in_word
        host='completion.amazon.co.uk'
    elif country=='de':
        url_add='https://completion.amazon.co.uk/search/complete?method=completion&mkt=4&l=de_DE&client=amazon-search-ui&search-alias=aps&qs=&cf=1&fb=1&sc=1&q='+in_word
        host='completion.amazon.co.uk'
    elif country=='it':
        url_add='https://completion.amazon.co.uk/search/complete?method=completion&mkt=35691&l=it_IT&client=amazon-search-ui&search-alias=aps&qs=&cf=1&fb=1&sc=1&q='+in_word
        host='completion.amazon.co.uk'
    elif country=='jp':
        url_add='https://completion.amazon.co.jp/search/complete?method=completion&l=ja_JP&client=amazon-search-ui&search-alias=aps&qs=&cf=1&fb=1&sc=1&mkt=6&q='+in_word
        host='completion.amazon.co.jp'
    elif country=='es':
        url_add='https://completion.amazon.co.uk/search/complete?method=completion&mkt=44551&l=es_ES&client=amazon-search-ui&search-alias=aps&qs=&cf=1&fb=1&sc=1&q='+in_word
        host='completion.amazon.co.uk'
    else:
        url_add='https://completion.amazon.co.uk/search/complete?method=completion&search-alias=aps&client=amazon-search-ui&mkt=3&fb=1&sc=1&q='+in_word
        host='completion.amazon.co.uk'

    page=get_url(url_add,host=host)
    return json.loads(page.text)[1]

