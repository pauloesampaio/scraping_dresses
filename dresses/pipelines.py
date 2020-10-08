# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json
import os

with open(os.path.join("credentials", "credentials.json")) as f:
    credentials = json.load(f)


class DressesPipeline(object):
    user_name = credentials["mongo_db"]["user"]
    user_password = credentials["mongo_db"]["password"]
    cluster_name = credentials["mongo_db"]["cluster"]
    db_name = credentials["mongo_db"]["database"]
    collection_name = credentials["mongo_db"]["collection"]

    def open_spider(self, spider):
        connector = (
            f"mongodb+srv://{self.user_name}:{self.user_password}"
            f"@{self.cluster_name}.qe0ku.gcp.mongodb.net/{self.db_name}?retryWrites=true&w=majority"
        )
        self.client = pymongo.MongoClient(connector)
        self.db = self.client[self.db_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].replace_one(
            {"_id": item["_id"]}, item, upsert=True
        )
        return item
