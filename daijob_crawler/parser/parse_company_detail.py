from collections.abc import Iterable

from salesnext_crawler.events import CrawlEvent, DataEvent, Event
from scrapy.http.response.html import HtmlResponse
from scrapy import Request
from daijob_crawler.schema.company import Company

CONTENT = {
    "本社国籍": "company_head_office",
    "所在国": "company_country_residence",
    "会社紹介": "company_description",
    "業種": "company_industry",
    "所在地": "company_address",
    "代表者": "company_representative",
    "設立年": "company_establish_date",
    "資本金": "company_capital",
    "従業員数": "company_employee_count",
    "事業内容": "company_business_content",
    "オフィスへのアクセス": "company_nearrest_station",
    "URL": "company_hp_url",  
}

def parse_company_detail(
    event: CrawlEvent[None, Event, HtmlResponse],
    response: HtmlResponse,
)->Iterable[Event]:
    
    data = Company(
        company_id = response.url.split('/')[-2],
        company_name = response.xpath("//div[@class='section01']//a/text()").get(),
    )
    
    labels = response.xpath("//table//tr//th//span/text()").getall()
    
    for label in labels:
        value = "".join([
        v.strip() for v in response.xpath(
            f"//table//tr//th[span/text()='{label}']/following-sibling::td//text()"
        ).getall() if v.strip()
    ])       
        for header, eng_text in CONTENT.items():
            if label == header:
                setattr(data, eng_text, value)
         
    
    yield DataEvent("companies", data)
    
    