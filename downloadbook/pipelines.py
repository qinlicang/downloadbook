# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class DownloadBookPipeline(object):
    conn = None
    cur = None

    def __init__(self):
        self.conn = sqlite3.connect('book.db')
        self.cur =  self.conn.cursor()
        # self.cur.execute('SELECT COUNT(*) FROM sqlite_master where type=\'table\' and name=\'book\'')
        self.cur.execute('create table if not exists book(title varchar(50),url varchar(50) primary key,content text)')
        
    # @classmethod
    # def from_crawler(cls, crawler):
    #     print('from_crawler')

    # def open_spider(self, spider):
    #     print('open_spider')

    # def close_spider(self, spider):
    #     print('close_spider')

    def process_item(self, item, spider):
        insert_sql = "insert into book(title, url) values (?,?)"
        try:
            self.cur.execute(insert_sql, (item['title'], item['url']))
            self.conn.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
            print('Could not complete operation:', e)
        return item