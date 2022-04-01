import requests
import json

source = 'https://api.github.com/users/vltian/repos'
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) "
                  "Gecko/20100101 Firefox/88.0"
}
repos = requests.get(source, headers=headers)

my_repos = json.loads(repos.text)

repos = []

for rep in my_repos:
    repos.append(rep["name"])
with open('rep_list.json', 'w') as json_file:
    json.dump(repos, json_file)