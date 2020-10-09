# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import datetime
import json


class GetDressesSpider(scrapy.Spider):
    name = "dresses_rc"
    allowed_domains = []
    current_page = 1
    start_urls = [
        f"https://api-gateway.riachuelo.com.br/ecommerce-catalogprovider-web-bff/v1/categories/19/products/?page={current_page}&sort=release-date&order=asc&mode=full&includeFilters=true"
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
            args={"lua_source": self.script, 
                  "wait": 5, 
                  'html': 1,
                  "headers": {
                      ":authority": "api-gateway.riachuelo.com.br",
                      ":method": "GET",
                  ":path": "/ecommerce-catalogprovider-web-bff/v1/categories/19/products/?page=1&sort=release-date&order=asc&mode=full&includeFilters=true",
                  ":scheme": "https",
                  "accept": "application/json",
                  "accept-encoding": "br",
                  "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                  "cache-control": "no-cache",
                    "channel": "web",
                    "origin": "https://www.riachuelo.com.br",
                    "referer": "https://www.riachuelo.com.br/feminino/colecao-feminino/vestido",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
                      "client_id": "e1b89be2-9d65-3031-b4f3-3fbb4230a450",
                      "access_token": "ebbdeafe-96ca-3494-9d49-be225900e713"
                  }},
        )
    def parse(self, response):
        print(f"Current page: {self.current_page}")
        text_response = response.data["html"]
        text_response = text_response.replace('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">', '')
        text_response = text_response.replace('</pre></body></html>', '')
        text_response = text_response.replace('\n', '')
        json_response = json.loads(text_response)
        import ipdb; ipdb.set_trace()
        for product in json_response.get("data").get("products"):
            yield {
                "_id": product["sku"],
                "product_retailer": self.name,
                "product_url": product["url"],
                "product_name": product["name"],
                "product_price": product["price"]["regular"],
                "product_images": [w for w in product["images"]],
                "crawl_date": datetime.datetime.utcnow(),
            }
        has_next_page = json_response["data"]["nextPage"]
        if has_next_page:
            self.current_page = self.current_page + 1
            next_page = f"https://api-gateway.riachuelo.com.br/ecommerce-catalogprovider-web-bff/v1/categories/19/products/?page={self.current_page}&sort=release-date&order=asc&mode=full&includeFilters=true"
            print("NEXT")
            yield SplashRequest(url=next_page,
                                callback=self.parse,
                                endpoint="render.json",
                                args={"lua_source": self.script, 
                                      "wait": 5, 
                                      'html': 1,
                                "headers": {
                      ":authority": "api-gateway.riachuelo.com.br",
                      ":method": "GET",
                  ":path": f"/ecommerce-catalogprovider-web-bff/v1/categories/19/products/?page={self.current_page}&sort=release-date&order=asc&mode=full&includeFilters=true",
                  ":scheme": "https",
                  "accept": "application/json",
                  "accept-encoding": "br",
                  "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                  "cache-control": "no-cache",
                    "channel": "web",
                    "origin": "https://www.riachuelo.com.br",
                    "referer": "https://www.riachuelo.com.br/feminino/colecao-feminino/vestido",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
                      "client_id": "e1b89be2-9d65-3031-b4f3-3fbb4230a450",
                      "access_token": "ebbdeafe-96ca-3494-9d49-be225900e713"
                  }}
                                )