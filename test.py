import requests
import re
from bs4 import BeautifulSoup

url = 'http://news.heraldcorp.com/view.php?ud=20200827000611'

res = requests.get(url)

bs = BeautifulSoup(res.text, 'html.parser')

data = bs.select('div.view_top_t2 ul li.ellipsis')

# time = re.search('[0-9]{4}[\.\-]?[0-9]{2}[\.\-]?[0-9]{2}', data).group()

print(data)