import scrapy
import pandas as pd
from bs4 import BeautifulSoup
from Package import FileMaker
import time
from tika import parser
from bs4 import BeautifulSoup
import requests

class ReportSpider(scrapy.Spider):

    name = "report"
    report_num = 0
    now_page = 1
    urls = [
        # 시황정보 0
        'https://finance.naver.com/research/market_info_list.nhn?&page={}',
        # 투자정보 1
        'https://finance.naver.com/research/invest_list.nhn?&page={}',
        # 종목분석 2
        'https://finance.naver.com/research/company_list.nhn?&page={}',
        # 산업분석 3
        'https://finance.naver.com/research/industry_list.nhn?&page={}',
        # 경제분석 4
        'https://finance.naver.com/research/economy_list.nhn?&page={}',
        # 채권분석 5
        'https://finance.naver.com/research/debenture_list.nhn?&page={}'
    ]
    temp = ''

    def start_requests(self):
        ReportSpider.fm = FileMaker.JsonMaker()
        ReportSpider.fm.create_folder()
        ReportSpider.fm.write_file()
        yield scrapy.Request(ReportSpider.urls[ReportSpider.report_num].format(ReportSpider.now_page), callback=self.parse)

    def close(self, reason):
        ReportSpider.fm.close_file()

    def parse(self, response):
        reports = response.css('table.type_1 tr').getall()[2:]
        if ReportSpider.temp == reports:
            return
        
        if reports != None:
            for report in reports:
                # 타임 브레이커
                # time.sleep(0.03)
                sp = BeautifulSoup(report, 'html.parser').select('td')
                
                try:
                    with open('bond.pdf', 'wb') as f:
                        f.write(requests.get(sp[2].select_one('a').attrs['href']).content)
                    contents = str(parser.from_file('bond.pdf')['content']).strip()

                    yield ReportSpider.fm.add_data({
                            # Datas
                            'name' : sp[0].text,
                            'company' : sp[1].text,
                            'content' : contents,
                            'date' : sp[3].text,
                            'click' : sp[4].text
                        })
                except:
                    continue
            # pdf_temp = requests.get(result.select_one('a').attrs['href'])

            # with open('bond.pdf', 'wb') as f:
            #     f.write(pdf_temp.content)

        ReportSpider.temp = reports
        ReportSpider.now_page +=1
        # yield scrapy.Request(ReportSpider.urls[ReportSpider.report_num].format(ReportSpider.now_page), callback=self.parse)
