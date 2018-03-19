import scrapy
import urllib.request
from lxml import etree
class DmozSpider(scrapy.Spider):
    name = "homePage"
    download_delay = 1
    start_urls = [
        'http://www.julive.com/project/s',
        'http://sh.julive.com/project/s',
        'http://tj.julive.com/project/s',
        'http://gz.julive.com/project/s',
        'http://cq.julive.com/project/s',
        'http://su.julive.com/project/s',
        'http://hz.julive.com/project/s',
        'http://cd.julive.com/project/s'
    ]

    def parse(self, response):
        regions = response.xpath(".//div[@class='nrpart show nrpart-area']//ul[@class='sel-value']/li/a/@href").extract()
        del regions[0]
        for region in regions:
            yield scrapy.Request(region,callback=self.page)

    def page(self,response):
        nextPages = response.xpath(".//div[@class='page']/ul[@class='pagination']/li[@class='next']/a/@href").extract()
        houses = response.xpath(".//div[@class='house-item main_click_total']")
        for house in houses:
            url = house.xpath(".//h4/a[@class='name project-card-item']/@href").extract()[0],
            position = house.xpath(".//div[@class='position project-card-position project-card-item']/span[@class='position-des']/a/text()").extract()[0]
            test = position[-3:-1]
            if test == '..':
                newPosition = self.getSet(url)
                if len(newPosition) == 2:
                    position = self.getSet(url)[1]
            yield {
            '城市名称':response.xpath(".//div[@class='header header-juli']/div[@class='inn']/div[@class='city-position city-tip']/span[@class='text']/text()").extract(),
            '小区名称':  house.xpath(".//h4/a[@class='name project-card-item']/text()").extract(),
            '销售状态' : house.xpath(".//h4/a[@class='tag-sale project-card-item']/text()").extract(),
            '位置' : position,
            '房屋类型' : house.xpath(".//div[@class='house-type']/div[@class='types']/a/text()").extract(),
            '更新时间' : house.xpath(".//div[@class='building-news']/p/span[@class='title']/text()").extract(),
            '售价/均价' : house.xpath(".//div[@class='price']/div[@class='total-price']/span[@class='number']/text()").extract(),
            '参考总价' : house.xpath(".//div[@class='price']/div[@class='developer']/span[@class='number']/text()").extract()
            }
        if nextPages != []:
            nextPages = response.urljoin(nextPages[0])
            yield scrapy.Request(nextPages, callback=self.page)

    def getSet(self,url):
        html = urllib.request.urlopen(url[0]).read()
        selector = etree.HTML(html)
        position = selector.xpath(".//div[@class='base-info']/ul[@class='info-list']/li/p[@class='txt']/a/text()")
        return (position)






