# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JuliItem(scrapy.Item):
    # 保存到数据库里面的字段
    id = scrapy.Field()  # 修改你所需要的字段
    city = scrapy.Field()
    image_url = scrapy.Field()
    house_name = scrapy.Field()
    price = scrapy.Field()  # 参考单价
    # tag = scrapy.Field()  # 标签
    type = scrapy.Field()  # 房屋类型
    address = scrapy.Field()  # 地址
    open_time = scrapy.Field()  # 开盘日期
    assess = scrapy.Field()  # 楼盘评价
    parking_lot = scrapy.Field()  # 车位
    property_company = scrapy.Field()  # 物业公司
    developers = scrapy.Field()  # 开发商
    property_fee = scrapy.Field()  # 物业费
    renovation = scrapy.Field()  # 装修
    house_info = scrapy.Field()  # 户型信息
