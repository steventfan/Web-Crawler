import sys
import os
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider

class crawler(CrawlSpider):
    name = 'crawler'
    rules = (Rule\
        (
            LinkExtractor(allow = (r'^https?:\/\/(www\.)?[^.]*\.gov[^.]*$')),
            callback = 'parse_page',
            follow = True
        ),)

    def __init__(self, url = None):
        super().__init__()
        self.start_urls = url

    def parse_page(self, response):
        try:
            global pages
            global filename
            global i
            if pages == 0:
                raise CloseSpider()
            f = open(filename, 'wb')
            f.write(response.body)
            f.close()
            i += 1
            filename = filename[0:len(directory + '/' + directory)] + str(i) + '.html'
            if pages > 0:
                pages -= 1
        except Exception:
            raise CloseSpider()

if len(sys.argv) < 3:
    print('[ERROR] Not enough parameters:\npython crawler.py <seed file> [# pages] [# levels] <output directory>')
    exit()
try:
    seed = open(sys.argv[1]).read().split()
except Exception:
    print('[ERROR] Failed to access seed file')
    exit()
directory = sys.argv[len(sys.argv) - 1]
pages = -1
levels = 0
if len(sys.argv) >= 4:
    try:
        pages = int(sys.argv[2])
    except Exception:
        print('[ERROR] Number of pages must be an integer')
        exit()
    if pages < 0:
        print('[SYSTEM] Interpreting negative number of pages as infinite')
    if(len(sys.argv) >= 5):
        try:
            levels = int(sys.argv[3])
        except Exception:
            print('[ERROR] Number of levels must be an integer')
            exit()
        if levels == 0:
            exit()                                                                                                  
        elif levels < 0:
            print('[SYSTEM] Interpreting negative number of levels as infinite')
            levels = 0
try:
    os.makedirs(directory, exist_ok = True)
except Exception:
    print('[ERROR] Failed to establish output directory')
    exit()
i = 0
filename = directory + '/' + directory + str(i) + '.html'
while os.path.isfile(filename):
    i += 1
    filename = filename[0:len(directory + '/' + directory)] + str(i) + '.html'
settings = get_project_settings()
settings.update({'DEPTH_LIMIT' : levels})
process = CrawlerProcess(settings)
spider = crawler()
process.crawl(spider, seed)
process.start()