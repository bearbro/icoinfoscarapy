# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class IcoinfoscarapyPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='icobenchdb',  # 数据库名
            user='root',  # 数据库用户名
            passwd='admin',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();

    def process_item(self, item, spider):
        self.cursor.execute(
            """insert into Icos_info(name, info_href, rate, other ,start, end,countries,restrictions_KYC,whitelist,
            page,subN,team,introduction,tags,whitepaper_url,about)
            value (%s, %s, %s, %s, %s, %s,%s,%s,%s,%s ,%s,%s,%s ,%s,%s ,%s) """,  # 纯属python操作mysql知识，不熟悉请恶补
            (item['name'],  # item里面定义的字段和表字段对应
             item['info_href'],
             item['rate'],
             item['other'],
             item['start'],
             item['end'],
             item['countries'],
             item['restrictions_KYC'],
             item['whitelist'],
             item['page'],
             item['subN'],
             item['team'] ,
             item['introduction'],
             item['tags'],
             item['whitepaper_url'],
             item['about']
             ))
        #name, info_href, rate, other ,start, end,countries,restrictions_KYC,whitelist
        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回