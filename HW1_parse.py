import requests
import json
from pathlib import Path

def get_response(url):
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
        time.sleep(0.5)

def parse_cat(url):
        response = get_response(url)
        data: dict = response.json()
        for pos in data:
            yield pos

def parse_prod(url):
    while url:
        response = get_response(url)
        data: dict = response.json()
        url = data["next"]
        for pos in data["results"]:
            yield pos

def get_save_path(dir_name: str) -> Path:
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path

def save(data: dict, file_path: Path):
    file_path.write_text(json.dumps(data, ensure_ascii=False))

'''Parameters definition'''
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
}

if __name__ == '__main__':
    cat_url = 'https://5ka.ru/api/v2/categories/'
    cat_path = get_save_path('categories')
    '''Parsing categories'''
    for cat in parse_cat(cat_url):
        a = cat['parent_group_code']
        '''Parsing products within categories'''
        prod_url: str = f'https://5ka.ru/api/v2/special_offers/?categories={a}&ordering=&page=1&price_promo__gte=&price_promo__lte=&100&search=&store'
        prod_list: list = []
        for prod in parse_prod(prod_url):
            prod_list.append(prod)
        prod_cat: list = [{"code": cat['parent_group_code']}, {"name": cat['parent_group_name']}, {"products": prod_list}]
        file_path = cat_path.joinpath(f"{a}.json")
        save(prod_cat, file_path)