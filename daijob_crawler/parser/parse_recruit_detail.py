from collections.abc import Iterable

from salesnext_crawler.events import CrawlEvent, DataEvent, Event
from scrapy.http.response.html import HtmlResponse
from scrapy import Request
from daijob_crawler.parser.parse_company_detail import parse_company_detail
from daijob_crawler.schema.recruit import Recruit


CONTENT = {
    "業種": "job_industry",
    "職種": "job_name_title",
    "企業名": "job_company_name_sub",
    "仕事内容": "job_description",
    "英語能力": "job_english_level",
    "日本語能力": "job_japanese_level",
    "年収": "job_salary",
    "休日休暇": "job_holiday",
    "契約期間": "job_contract_period",
    "応募条件": "job_working_hours",
    "休日": "job_holiday",
    "最寄り駅": "job_nearest_station",
    "(社風など）": "job_company_business_content",
    "給与に関する説明": "job_salary",
    "見込み年収": "job_salary",
    "時給": "job_salary",
    "韓国語能力": "job_korean_level",
    "勤務時間": "job_working_hours",
    "取扱い会社": "job_company_name",
    "この求人の": "job_feature",
    "勤務地": "job_location",
    '企業について': "job_company_business_content",

    
}
def parse_recruit_detail(
    event: CrawlEvent[None, Event, HtmlResponse],
    response: HtmlResponse,
    
) -> Iterable[Event]:
    
    crawled_company_ids = event.metadata["crawled_company_ids"]
    crawled_recruit_ids = event.metadata["crawled_recruit_ids"]
    data = Recruit(

    source_job_url  =  response.url,
    job_id = response.url.split('/')[-1],
    job_title = response.xpath("normalize-space(//h1[@class='seo_keyword']/text())").get(),
    job_category = [item.strip() for item in response.xpath("//div[@class='jobs_box_header_category']/ul//li/a/span/text()").getall()],
    job_category_ids = response.xpath("//div[@class='jobs_box_header_category']/ul//li/a/@href").getall(),
    job_last_updated = response.xpath("//div[@class ='jobs_box_header_date']//span[@class='roboto']/text()").get(),
    )
    categories = []
    job_category = response.xpath("//div[@class='jobs_box_header_category']//ul//li//a/span")
    for category in job_category:
        cat = category.xpath("normalize-space(./text())").get()
        categories.append(cat)
    data.job_category = categories
        
    labels = response.xpath("//table//tr//th//span/text()").getall()
    
    # missing_labels = list(labels-CONTENT.keys())
    # print(f"Missing labels: {missing_labels}")
    
    for label in labels:
        value = "".join([
        v.strip() for v in response.xpath(
            f"//table//tr//th[span/text()='{label}']/following-sibling::td//text()"
        ).getall() if v.strip()
    ])
       
        for header, eng_text in CONTENT.items():
            if label == header:
                if header == "仕事内容":
                    value = "".join(response.xpath("//table//tr//th[span//text()='仕事内容']/following-sibling::td/text()").getall())
                setattr(data, eng_text, value)
             
    data.job_company_url = response.xpath("//p[@class='treatment_btn01']//a/@href").get()
    data.job_company_id = data.job_company_url.split('/')[-2]
    yield DataEvent("recruit", data)

    if data.job_company_id not in event.metadata["crawled_company_ids"]:       
        yield CrawlEvent(
            request=Request("https://www.daijob.com"+ data.job_company_url),
            metadata={
                'crawled_company_ids': crawled_company_ids,
                'crawled_recruit_ids': crawled_recruit_ids,},
            callback=parse_company_detail,
        )
        event.metadata["crawled_company_ids"].append(data.job_company_id)
    related_job = response.xpath("//p[@class='treatment_btn02']//a/@href").get()
    if data.job_company_id and data.job_id:    
        from daijob_crawler.parser.parse_recruit_list import parse_recruit_list
        yield CrawlEvent(
            request=Request("https://www.daijob.com"+ related_job),
            metadata={
                "crawled_company_ids": crawled_company_ids,
                "crawled_recruit_ids": crawled_recruit_ids,
            },
            callback=parse_recruit_list,
        )
    
    
    