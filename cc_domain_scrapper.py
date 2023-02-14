import requests
import re

cc_url = 'http://index.commoncrawl.org/collinfo.json'
url_to_check = "https://onet.pl"
output_file = "onet.txt"

# get the index information
response = requests.get(cc_url)
index_info = response.json()

# create a set to store the URLs we've found
urls = set()
indexes = []

# iterate over the indexes and search for the URL
index_ids = [info['id'] for info in index_info if 'CC-MAIN-' in info['id'] and int(info['id'][8:12]) >= 2000]

for index in index_ids:
    print(index)
    cc_url = 'http://index.commoncrawl.org/' + index + '-index?url={}/*&output=json'.format(url_to_check)
    try:
        response = requests.get(cc_url)
        response.raise_for_status()
        urls.update(re.findall('"url": "([^"]+)"', response.text))
    except Exception as e:
        print("err: ",e)
        pass

with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(urls))
