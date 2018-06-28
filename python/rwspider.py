import scrapy

class RunningWarehouseSpider(scrapy.Spider):
  name = 'runningwarehouse'
  allowed_domains = ['runningwarehouse.com']
  start_urls = ['https://www.runningwarehouse.com/']

  def parse(self, response):
    page = response.url.split("/")[-2]
    filename = 'quotes-%s.html' % page
    with open(filename, 'wb') as f:
      f.write(response.body)
    self.log('Saved file %s' % filename)
