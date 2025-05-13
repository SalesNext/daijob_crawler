from collections.abc import Iterable
from enum import Enum
from daijob_crawler.parser.parse_recruit_list import parse_recruit_list
from salesnext_crawler.crawler import ScrapyCrawler
from salesnext_crawler.events import CrawlEvent, Event, SitemapEvent
from scrapy import Request
import pyarrow as pa    

class CrawlType(str,Enum):
    CRAWL_FROM_TYPE = "CRAWL_FROM_TYPE"
    CRAWL_FROM_PREFECTURE = "CRAWL_FROM_PREFECTURE"
    CRAWL_FROM_MASTER_COMPANY = "CRAWL_FROM_MASTER_COMPANY"
    
class DaijobCrawler(ScrapyCrawler):
    def __init__(self, daily: bool = False, timeout: int = 1800,
                 crawl_type : list[CrawlType] = [CrawlType.CRAWL_FROM_MASTER_COMPANY,
                                                 ]) -> None:
        self.daily = daily
        self.crawl_type = crawl_type
    def start(self) -> Iterable[Event]: 
       yield CrawlEvent(
           request=Request("https://www.daijob.com/jobs/search_result?job_post_language=2&submit.x=28&submit.y=10&page=1&sort_order=3"),
           metadata= None , 
           callback= parse_recruit_list,
       )
       
      
       
           
      
        

