import scrapy
from datetime import datetime

class FinancialNewsSpider(scrapy.Spider):
    name = "financial_news"
    
    def __init__(self, *args, **kwargs):
        super(FinancialNewsSpider, self).__init__(*args, **kwargs)
        self.platforms = [
            {"name": "Bloomberg", "url": "https://www.bloomberg.com/markets"},
            {"name": "Reuters", "url": "https://www.reuters.com/business/finance/"},
            {"name": "WallStreetCn", "url": "https://wallstreetcn.com/news/global"},
            # ... add more up to 20+
        ]

    def start_requests(self):
        for platform in self.platforms:
            yield scrapy.Request(url=platform['url'], callback=self.parse, meta={'platform': platform['name']})

    def parse(self, response):
        """
        Generic parsing logic (to be overridden for specific platforms)
        """
        # This is a placeholder for actual extraction logic
        # In production, each platform would have its own spider or specialized parser
        articles = response.css('article')
        for article in articles:
            item = {
                'title': article.css('h3::text').get(),
                'url': response.urljoin(article.css('a::attr(href)').get()),
                'platform': response.meta['platform'],
                'timestamp': datetime.now().isoformat(),
                'content_snippet': article.css('p::text').get()
            }
            if item['title']:
                yield item
