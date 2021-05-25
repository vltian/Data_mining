import requests
import json
from pathlib import Path

'''Parameters definition'''
cat_link = 'https://5ka.ru/api/v2/categories/'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
}

'''Parsing categories'''
response_cat = requests.get(cat_link, headers=headers)
data = response_cat.json()

'''Parsing products within categories'''
for i in data:
    a = i['parent_group_code']
    response = requests.get(f'https://5ka.ru/api/v2/special_offers/?categories={a}&ordering=&page=1&price_promo__gte=&price_promo__lte=&100&search=&store')
    cat_prod: dict = cat_prod.append
