
import requests
import pandas as pd
from tqdm import tqdm
import json
from bs4 import BeautifulSoup

url = 'https://finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_CORP03Y&page={}'

data_list = []
for i in tqdm(range(1, 600)):
    # print(i)
    page_url = url.format(i)

    res = requests.get(page_url)
    bs = BeautifulSoup(res.text, 'html.parser')

    datas = bs.select('tbody tr')

    for data in datas:

        data_dict = {}

        date = data.select('td.date')[0].text.strip()
        num_data = data.select('td.num')[0].text.strip()

        data_dict['date'] = date
        data_dict['rate'] = num_data

        data_list.append(data_dict)

df = pd.DataFrame(data_list)
print(df.head())
df.to_json('cb_rate.json')
# print(data_list)