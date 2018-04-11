import scrapy
import urllib.request
from lxml import etree
from juli.items import JuliItem
import re
class DmozSpider(scrapy.Spider):
    name = "homePage"
    download_delay = 1
    start_urls = [
        'http://www.julive.com/project/s'
        # 'http://sh.julive.com/project/s',
        # 'http://tj.julive.com/project/s',
        # 'http://gz.julive.com/project/s',
        # 'http://cq.julive.com/project/s',
        # 'http://su.julive.com/project/s',
        # 'http://hz.julive.com/project/s',
        # 'http://cd.julive.com/project/s'
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
            yield scrapy.Request(url[0],self.getHouseInfo)

        # if nextPages != []:
        #     nextPages = response.urljoin(nextPages[0])
        #     yield scrapy.Request(nextPages, callback=self.page)

    # def getSet(self,url):
    #     html = urllib.request.urlopen(url[0]).read()
    #     selector = etree.HTML(html)
    #     position = selector.xpath(".//div[@class='base-info']/ul[@class='info-list']/li/p[@class='txt']/a/text()")
    #     return (position)

    def getHouseInfo(self,response):
        item = JuliItem()
        item['id'] = re.sub(r'\D', "", response.url)
        titel = response.xpath(".//div[@class='center']/div[@class='row row-crumb']/ul[@class='crumb']/li/a/text()").extract()
        item['city'] = titel[1].replace("楼盘","")
        item['image_url'] = response.xpath(".//div[@class='row']/div[@class='focus']/div[@class='albums-detail']/div[@class='albums']/div[@class='content']/div[@class='slide']/ul[@class='slide-ul']/li/a/img/@src").extract()[0]
        item['house_name'] = response.xpath(".//div[@class='center']/div[@class='row row-top-nav']/div[@class='top-menu-wrap']/div[@class='house-name']/div[@class='name']/h1/text()").extract()[0]
        # price = response.xpath(".//div[@class='house-info house-info-a']/div[@class='base-info']/ul[@class='info-list']/li/div[@class='info-list']/em/text()").extract()
        item['open_time'] = response.xpath(".//div[@class='house-info house-info-a']/div[@class='base-info']/ul[@class='info-list']/li[@class='date']/p[@class='txt']/text()").extract()[0]

        haveHouseInfo = response.xpath(".//div[@class='house-info house-info-a']/div[@class='base-info']/ul[@class='info-list']/li/p[@class='txt']/a/text()").extract()[0]
        detailUrl = response.xpath(".//div[@class='detail-nav detail-nav-nine']/ul/li/a/@href").extract()[7]
        htDetailUrl = response.xpath(".//div[@class='detail-nav detail-nav-nine']/ul/li/a/@href").extract()[1]
        exportcomUrl = response.xpath(".//div[@class='detail-nav detail-nav-nine']/ul/li/a/@href").extract()[4]
        if haveHouseInfo != '':
            yield scrapy.Request(htDetailUrl,meta={'item':item,'detailUrl':detailUrl,'exportcomUrl':exportcomUrl},callback=self.getHouseType)



        # print (item)

    def getHouseDetail(self,response):
        item = response.meta['item']
        baseInfo = response.xpath(".//div[@class='center']/div[@class='row row-baseinfo']/div[@class='col5-wrap']/div[@class='col5']/div[@class='box box-base']/div[@class='bd']")
        item['address'] = baseInfo.xpath(".//ul[@class='base-info-list']/li/div[@class='txt']/p/text()").extract()
        item['type'] = baseInfo.xpath(".//ul[@class='base-info-list']/li/div[@class='txt']/p/text()").extract()[2]
        item['developers'] = baseInfo.xpath(".//ul[@class='base-info-list']/li/div[@class='txt']/p/text()").extract()[5]
        item['price'] = response.xpath(".//div[@class='row row-baseinfo']/div[@class='col5-wrap']/div[@class='col5']/div[@class='box box-sale']/div[@class='bd']/ul[@class='base-info-list']/li/div[@class='txt']/p/text()").extract()[0]
        houseDetail = response.xpath(".//div[@class='row row-baseinfo']/div[@class='col5-wrap']/div[@class='col5']/div[@class='box house-details']/div[@class='bd']")
        item['property_company'] = houseDetail.xpath(".//ul[@class='base-info-list']/li/div[@class='txt']/p/text()").extract()[0]
        item['property_fee'] = houseDetail.xpath(".//ul[@class='base-info-list']/li/div[@class='txt']/p/text()").extract()[1]
        item['parking_lot'] = houseDetail.xpath(".//ul[@class='base-info-list']/li/div[@class='txt']/p/text()").extract()[5]
        item['renovation'] = houseDetail.xpath(".//ul[@class='base-info-list']/li/div[@class='txt']/p/text()").extract()[7]
        exportcomUrl = response.meta['exportcomUrl']
        if exportcomUrl !='':
            yield scrapy.Request(exportcomUrl,meta={'item':item},callback=self.getHouseAssess)


    def getHouseAssess(self,response):
        item = response.meta['item']
        item['assess'] = response.xpath(".//div[@class='dp-detail']/div[@class='dp-base data-short']/p/text()").extract()
        yield item

    def getHouseType(self,response):
        item = response.meta['item']
        house_info = []
        houseTypes = response.xpath(".//div[@class='row']/div[@class='house-analysis']/div[@class='bd']/div[@class='htype-list card-list-box']/div[@class='house-type-item']")
        for houseType in houseTypes:
            houseTitel = houseType.xpath(".//div[@class='media-house-type']/div[@class='text']/div[@class='house-type-name']/h4/a/text()").extract()[0]
            houseTypeName = houseTitel.split(" ")[0]
            area = houseTitel.split(" ")[1]
            sellStatus = houseType.xpath(".//div[@class='media-house-type']/div[@class='text']/div[@class='house-type-name']/ul[@class='ht-tag']/li/text()").extract()[0]
            Orientation = houseType.xpath(".//div[@class='media-house-type']/div[@class='text']/ul[@class='ht-info']/li/div[@class='td']/text()").extract()[0]
            image = houseType.xpath(".//div[@class='media-house-type']/div[@class='pic']/a/img/@src").extract()
            introduce = houseType.xpath(".//div[@class='media-house-type']/div[@class='text']/div[@class='unit-analysis']/div[@class='td']/p[@class='txt']/text()").extract()
            tag = '无'
            house_info.append({'houseTypeName':houseTypeName,'area':area,'sellStatus':sellStatus,'Orientation':Orientation,'image':image,'introduce':introduce,'tag':tag})
        item['house_info'] = str(house_info)
        detailUrl = response.meta['detailUrl']
        exportcomUrl = response.meta['exportcomUrl']
        if detailUrl != '':
            yield scrapy.Request(detailUrl,meta={'item':item,'exportcomUrl':exportcomUrl},callback=self.getHouseDetail)


