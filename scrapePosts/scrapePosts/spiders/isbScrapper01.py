from pandas.core.algorithms import mode
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin
import pandas as pd

class ImagesSpider(scrapy.Spider):

    name = 'isb_scrapper'

    start_urls = ['https://www.dltinteriordesigns.com/portfolio/']

    def parse(self, response):
        texts = response.css('.edgtf-pli-text h6::text').getall()
        links = response.css('.edgtf-pli-link::attr(href)').getall()
        total_data = pd.DataFrame()
        for i in range(len(texts)):
          if 'In Progress' not in texts[i]:
            url = urljoin(response.url, links[i])
            yield scrapy.Request(url, callback=self.parse_product)
            df = pd.read_csv('Total_Data.csv')
            df['Categories'] = 'Category_'+str(i)
            df.to_csv('Islamabad/Category_'+str(i)+'.csv', index=False)

    def parse_product(self, response):
      df = pd.DataFrame()
      images = response.css('.edgtf-ps-image a::attr(href)').getall()
      df['Images'] = images
      df['City'] = 'Islamabad'
      df['Styles'] = ['accessories_style_'+str(i) for i in range(len(images))]
      df.drop(df.index[-1])
      df.to_csv('Total_Data.csv', index=False)
      print('Done')

if __name__ == "__main__":
  process = CrawlerProcess()
  process.crawl(ImagesSpider)
  process.start()