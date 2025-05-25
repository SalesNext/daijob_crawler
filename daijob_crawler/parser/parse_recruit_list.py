from collections.abc import Iterable
import math
from salesnext_crawler.events import CrawlEvent, DataEvent, Event
from scrapy.http.response.html import HtmlResponse
from scrapy import Request
from daijob_crawler.parser.parse_recruit_detail import parse_recruit_detail
import re

def parse_recruit_list(
    event: CrawlEvent[None, Event, HtmlResponse],
    response: HtmlResponse,
    
) -> Iterable[Event]:
    crawled_company_ids = event.metadata["crawled_company_ids"]
    crawled_recruit_ids = event.metadata["crawled_recruit_ids"]
    job_url = response.xpath("//div[@class='jobs_box mb16']//a/@href").getall()
    total_page = int(response.xpath("//span[@class='roboto']/text()").get())
    page = total_page / 20
    page = math.ceil(page)
    urls = []
    for url in job_url:
        if 'jobs/detail/' in url:
            urls.append(url)
    urls = list(set(urls))
    next_page = response.xpath("//li[@class='next']/a/@href").get()
    next_page = response.urljoin(next_page)
    if page:
        for i in range(2, page):
           yield CrawlEvent(
                request=Request(f"https://www.daijob.com/jobs/search_result?job_post_language=2&job_search_form_hidden=1&page={i}"),
                metadata={
                    "crawled_company_ids": crawled_company_ids,
                    "crawled_recruit_ids": crawled_recruit_ids,
                },
                callback=parse_recruit_list,
            ) 
            
    for url in urls:
        url = 'https://www.daijob.com' + url
        recruit_id = url.split('/')[-1]
        if recruit_id not in event.metadata["crawled_recruit_ids"]:
            crawled_recruit_ids.append(recruit_id)
            yield CrawlEvent(
                request= Request(url = url),
                metadata = {'crawled_recruit_ids': crawled_recruit_ids,
                            'crawled_company_ids': crawled_company_ids},
                callback= parse_recruit_detail,
            )
