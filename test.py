import requests
import re
from bs4 import BeautifulSoup

url = 'https://www.fnnews.com/news/202008241022222988'

res = requests.get(url)

bs = BeautifulSoup(res.text, 'html.parser')

data = bs.select('div.view_hd div.byline')

# time = re.search('[0-9]{4}[\.\-]?[0-9]{2}[\.\-]?[0-9]{2}', data).group()

print(data)