# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MyscrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonPipeline(object):
    def process_item(self, item, spider):
         base_dir = os.getcwd()
         filename = base_dir + '/news.json'
         # 打开json文件，向里面以dumps的方式吸入数据
         # 注意需要有一个参数ensure_ascii=False ，不然数据会直接为utf编码的方式存入比如
         # :“/xe15”
         with codecs.open(filename, 'a') as f:
             line = json.dumps(dict(item), ensure_ascii=False) + '\n'
             f.write(line)
         return item