import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

class ImagesSpider(scrapy.Spider):
    
    name = 'rwp_images'

    start_urls = [
        'https://kitandkaboodle.com/living/',
        'https://kitandkaboodle.com/dining/',
        'https://kitandkaboodle.com/bedrooms/',
        'https://kitandkaboodle.com/accessories/'
    ]

    def parse(self, response):
        df = pd.DataFrame()
        category = response.url.split('/')[-2]
        count = 0
        cats = []
        images = []
        styles = []
        city = []
        image_divs = response.css('.wd-images-gallery div a img::attr(src)').getall()
        for i in image_divs:
            count = count + 1
            cats.append(category)
            images.append(i)
            styles.append(category+'_style_'+str(count))
            city.append('Rawalpindi')
        df['Images'] = images              
        df['City'] = city
        df['Categories'] = cats
        df['Styles'] = styles
        print(df)
        df.to_csv(f'Rawalpindi/{category}.csv', index=False)

if __name__ == "__main__":
  process = CrawlerProcess()
  process.crawl(ImagesSpider)
  process.start()