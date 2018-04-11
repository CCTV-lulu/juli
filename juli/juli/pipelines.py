
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import psycopg2


class JuliPipeline(object):
    '''保存到数据库中对应的class
           1、在settings.py文件中配置
           2、在自己实现的爬虫类中yield item,会自动执行'''

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用'''
        dbparams = dict(
            host='127.0.0.1',  # 读取settings中的配置
            database='houseData',
            user='postgres',
            password='password',
            port=5432,
        )
        dbpool = adbapi.ConnectionPool('psycopg2', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    def _conditional_insert(self, txn, item):
        params = (item["id"], item["city"], item["image_url"], item["house_name"], item["price"], item["type"],
                  item["renovation"], item["address"], item["house_info"], \
                  item['open_time'], item['assess'], item['parking_lot'], item['property_company'], item['developers'],
                  item['property_fee'])
        txn.execute("insert into newhouse(id,city,image_url,house_name,price,type,renovation,address,house_info,open_time,assess,parking_lot,property_company,developers,property_fee) \
                                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);COMMIT", params)

    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print ('--------------database operation exception!!-----------------')
        print ('-------------------------------------------------------------')
        print (failue)
