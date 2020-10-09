# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import datetime


class GetDressesSpider(scrapy.Spider):
    name = "dresses_rn"
    allowed_domains = ["lojasrenner.com.br"]
    start_urls = [
        "https://www.lojasrenner.com.br/c/feminino/vestidos/-/N-cg003xZ1hwylc0/p1"
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
                html = splash:html(),
            }
        end
    """

    def start_requests(self):
        yield SplashRequest(
            url=self.start_urls[0],
            callback=self.parse,
            endpoint="execute",
            args={"lua_source": self.script},
        )

    def parse(self, response):
        product_urls = response.xpath('//div[@class="subject"]/a/@href').getall()
        yield from response.follow_all(product_urls, self.parse_product)
        next_page = response.xpath(
            '//span[@class="js-align-center pagination-buttons-wrapper"]/a[@class="js-next-paginator"]/@href'
        ).get()
        if next_page:
            yield SplashRequest(
                url=next_page,
                callback=self.parse,
                endpoint="execute",
                args={"lua_source": self.script},
            )


    def parse_price(self, product_price):
        product_price = product_price.replace(",",".")
        product_price = product_price.replace("R$","")
        product_price = float(product_price)
        return product_price
   

    def parse_product(self, response):
        product_images = response.xpath(
            '//div[@class="main_product_image"]/div[@id="productGalery"]/div/img/@src'
        ).getall()
        product_url = response.url
        product_sku = int(product_url.split("sku=")[-1])
        product_price = response.xpath(
            '//div[@class="main_product_info"]/div/div[@id="js-div-buy"]/span/div/span/text()'
            ).get()
        if product_price:
            product_price = self.parse_price(product_price)
        yield {
            "_id": product_sku,
            "product_retailer": self.name,
            "product_url": product_url,
            "product_name": response.xpath(
                '//div[@class="main_product_info"]/div[@class="product_details"]/h1/span/text()'
            ).get(),
            "product_price": product_price,
            "product_images": [response.urljoin(w) for w in product_images],
            "crawl_date": datetime.datetime.utcnow(),
        }
