# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import datetime
import json


class GetDressesSpider(scrapy.Spider):
    name = "dresses_am"
    allowed_domains = []
    start_urls = [
        "https://api.c6mp-areosltdb1-p1-public.model-t.cc.commerce.ondemand.com/amaroecpcommercewebservices/v2/amaro-br/products/search?query=:date:department:roupas-femininas:category:vestidos&pageSize=48&currentPage=0&fields=FULL&curr=BRL&lang=pt"
    ]

    script = """
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(0.5))
            splash:set_viewport_full()
            assert(splash:wait(5.0))
            return {
                html = splash:json(),
            }
        end
    """

    def start_requests(self):
        yield SplashRequest(
            url=self.start_urls[0],
            callback=self.parse,
            endpoint="render.json",
            args={"lua_source": self.script, "wait": 5, 'html': 1},
        )

    def parse(self, response):
        text_response = response.data["html"]
        text_response = text_response.replace('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">', '')
        text_response = text_response.replace('</pre></body></html>', '')
        text_response = text_response.replace('\n', '')
        json_response = json.loads(text_response)
        for product in json_response.get("products"):
            yield {
                "_id": product["code"],
                "product_retailer": self.name,
                "product_url": product["url"],
                "product_name": product["name"],
                "product_price": product["prices"]["nowPrice"]["value"],
                "product_images": [w["url"] for w in product["images"]],
                "crawl_date": datetime.datetime.utcnow(),
            }
        current_page = json_response.get("pagination").get("currentPage")
        total_pages = json_response.get("pagination").get("totalPages")-1
        print(f"crawler page {current_page} out of {total_pages}")
        if current_page < total_pages:
            next_page = f"https://api.c6mp-areosltdb1-p1-public.model-t.cc.commerce.ondemand.com/amaroecpcommercewebservices/v2/amaro-br/products/search?query=:date:department:roupas-femininas:category:vestidos&pageSize=48&currentPage={current_page+1}&fields=FULL&curr=BRL&lang=pt"
            print(f"next_page_url: {next_page}")
            print("NEXT")
            yield SplashRequest(url=next_page,
                                callback=self.parse,
                                endpoint="render.json",
                                args={"lua_source": self.script, 
                                      "wait": 5, 
                                      'html': 1
                                      }
                                )