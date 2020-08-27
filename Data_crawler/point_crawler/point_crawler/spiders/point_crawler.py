import scrapy
import pandas as pd
from bs4 import BeautifulSoup
from Package import FileMaker
import time

class PointSpider(scrapy.Spider):

    name = "point"
    temp = pd.read_csv('./url_list.csv')
    point_names = temp['NAME']
    point_urls = temp['URLs']
    point_number = 0
    MAX_point = len(point_names)
    now_page = 1
    # max_page = 0

    def start_requests(self):
        PointSpider.fm = FileMaker.JsonMaker()
        PointSpider.fm.create_folder()
        PointSpider.fm.write_file()
        yield scrapy.Request(PointSpider.point_urls[PointSpider.point_number] + '&page=1', callback=self.parse)

    def close(self, reason):
        PointSpider.fm.close_file()

    def parse(self, response):
        points = response.css('tbody tr').getall()
        if points != None:
            for point in points:
                sp = BeautifulSoup(point, 'html.parser').text.split()
                # 타임 브레이커
                time.sleep(0.03)
                yield PointSpider.fm.add_data({
                        # Datas
                        'name' : PointSpider.point_names[PointSpider.point_number],
                        'date' : sp[0],
                        'target' : sp[1]
                    })

        # 페이지 끝이 아니면,
        if len(points) == 10:
            PointSpider.now_page += 1
            yield scrapy.Request(PointSpider.point_urls[PointSpider.point_number]+ '&page={}'.format(PointSpider.now_page), callback=self.parse)
        # 페이지 끝이면,
        else:
            PointSpider.now_page = 1
            PointSpider.point_number += 1
            yield scrapy.Request(PointSpider.point_urls[PointSpider.point_number]+ '&page=1', callback=self.parse)
