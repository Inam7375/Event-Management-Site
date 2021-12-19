import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

class ImagesSpider(scrapy.Spider):
    
    name = 'rwp_images'

    start_urls = [
        'https://shazeinteriors.com/kitchen-design.html',
        'https://shazeinteriors.com/interior-designs.html',
        'https://shazeinteriors.com/wardrobes.html',
        'https://shazeinteriors.com/floors.html'
    ]

    def parse(self, response):
        df = pd.DataFrame()
        url = response.url.split('/')[-2]
        data = response.url.split('.')[-2]
        data = data.split('/')[-1]
        if len(data.split('-')) > 1:
            category = data.split('-')[0]
        else:
            category = data
        count = 0
        number = []
        cats = []
        images = []
        styles = []
        city = []
        image_divs = response.css('.gallery-grids div img::attr(src)').getall()
        for i in image_divs:
            count = count + 1
            cats.append(category)
            number.append('0300-5557300')
            images.append(url + '/' + i)
            styles.append(category+'_style_'+str(count))
            city.append('Rawalpindi')
        df['Images'] = images              
        df['City'] = city
        df['Categories'] = cats
        df['Styles'] = styles
        print(df)
        df.to_csv(f'../../Islamabad/{category}01.csv', index=False)

if __name__ == "__main__":
  process = CrawlerProcess()
  process.crawl(ImagesSpider)
  process.start()