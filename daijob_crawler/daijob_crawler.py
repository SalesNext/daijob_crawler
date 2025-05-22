from collections.abc import Iterable
from enum import Enum
from daijob_crawler.parser.parse_recruit_list import parse_recruit_list
from salesnext_crawler.crawler import ScrapyCrawler
from salesnext_crawler.events import CrawlEvent, Event, SitemapEvent
from scrapy import Request
import pyarrow as pa    

class DaijobCrawler(ScrapyCrawler):
    def __init__(self, daily: bool = False, timeout: int = 1800,
                 ) -> None:
        self.daily = daily
     
    def start(self) -> Iterable[Event]: 
       crawled_company_ids = []
       crawled_recruit_ids = []
       if self.daily:
            crawled_recruit_table : pa.Table = self.readers["recruit"].read()
            crawled_recruit_ids = crawled_recruit_table.select(["job_id"]).drop_null().to_pydict()["job_id"]
            crawled_recruit_ids = list(crawled_recruit_ids)
            
            crawled_company_table : pa.Table = self.readers["company"].read()
            crawled_company_ids = crawled_company_table.select(["company_id"]).drop_null().to_pydict()["company_id"]
            crawled_company_ids = list(crawled_company_ids) 
       
       
       
       yield CrawlEvent(
            request=Request(f"https://www.daijob.com/jobs/search_result?job_post_language=2&job_search_form_hidden=1&page=1&sort_order=3"),
            metadata= {
                "crawled_company_ids": crawled_company_ids,
                "crawled_recruit_ids": crawled_recruit_ids,
            }, 
            callback= parse_recruit_list,
        )
       
      
       
           
      
        

