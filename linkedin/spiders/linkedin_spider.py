from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from linkedin.items import LinkedinItem

class LinkedinSpider(CrawlSpider):
  name = "linkedin"
  allowed_domains = ["linkedin.com"]
  '''
  centilist_one = [i for i in xrange(1,100)]
  centilist_two = [i for i in xrange(1,100)]
  centilist_three = [i for i in xrange(1,100)]
  start_urls = ["http://www.linkedin.com/directory/people-%s-%d-%d-%d" 
                % (alphanum, num_one, num_two, num_three) 
                  for alphanum in "abcdefghijklmnopqrstuvwxyz"
                  for num_one in centilist_one
                  for num_two in centilist_two
                  for num_three in centilist_three
                ]
  '''
  start_urls = ["http://www.linkedin.com/directory/people-a-23-23-2"]

  rules = (
      Rule(SgmlLinkExtractor(allow=('\/pub\/.+', ))
                            , callback='parse_item'),
  )

  def parse_item(self, response):
    if response:
      hxs = HtmlXPathSelector(response)
      item = LinkedinItem()
      item['name'] = hxs.select('//span/span/text()').extract()
      
      # parse list of duplicate profile
      if not item['name']:
        # NOTE: Results page only displays 25 of possibly many more names;
        # LinkedIn requests authentication to see the rest. Need to resolve
        multi_profile_urls = hxs.select('//*[@id="result-set"]/li/h2/strong/ \
                                          a/@href').extract()
        for profile_url in multi_profile_urls:
          yield Request(profile_url, callback=self.parse_item)
      
      else:
        # all of this should be handles in pipeline?
        first_name = item["name"][0]
        last_name = item["name"][2]
        # insert into database
