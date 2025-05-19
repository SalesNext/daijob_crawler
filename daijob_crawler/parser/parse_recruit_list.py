from collections.abc import Iterable

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
    urls = []
    for url in job_url:
        if 'jobs/detail/' in url:
            urls.append(url)
    urls = list(set(urls))
    next_page = response.xpath("//li[@class='next']/a/@href").get()
    next_page = response.urljoin(next_page)
    if next_page:
        yield CrawlEvent(
            request=Request(next_page),
            metadata={'crawled_recruit_ids': crawled_recruit_ids,
                      'crawled_company_ids': crawled_company_ids},
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
