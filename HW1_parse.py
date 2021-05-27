import json
import time
from pathlib import Path
import requests

class Parse:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    params = {
    }

    def __init__(self, url, save_path: Path):
        self.url = url
        self.save_path = save_path

    def _get_response(self, url):
        while True:
            response = requests.get(url, params=self.params, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.5)

    def run(self):
        for cat in self._parse(self.url):
            a = cat['parent_group_code']
            prod_url: str = f'https://5ka.ru/api/v2/special_offers/?categories={a}&ordering=&page=1&price_promo__gte=&price_promo__lte=&100&search=&store'
            prod_list1: list = []
            for prod in self._parse1(prod_url):
                prod_list1.append(prod)
            prod_list: list = [{"code": cat['parent_group_code']}, {"name": cat['parent_group_name']}, {"products": prod_list1}]
#           cat['product'] = [prod_list]
            print (prod_list)
            file_path = self.save_path.joinpath(f"{a}.json")
            self._save(prod_list, file_path)

    def _parse(self, url):
 #       while url:
            response = self._get_response(url)
            data: dict = response.json()
            print (data)
 #          url = data["next"]
            for pos in data:
                yield pos

    def _parse1(self, url):
#       while url:
        response = self._get_response(url)
        data: dict = response.json()
#       url = data["next"]
        for pos in data["results"]:
            yield pos

    def _save(self, data: dict, file_path: Path):
        file_path.write_text(json.dumps(data, ensure_ascii=False))

def get_save_path(dir_name: str) -> Path:
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path

if __name__ == '__main__':
    url = "https://5ka.ru/api/v2/categories/"
    product_path = get_save_path('categories')
    parser = Parse(url, product_path)
    parser.run()