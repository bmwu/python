import scrapy

class BaiduSpider(scrapy.Spider):
    name = "baidu"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "https://pan.baidu.com/share/home?uk=1&view=share#category/type=0",
        "https://pan.baidu.com/share/home?uk=2&view=share#category/type=0"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)