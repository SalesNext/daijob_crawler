from typing import Optional, List

from pydantic import BaseModel

fack = {
    "業種": "job_industry",
    "職種": "job_name_title",
    "企業名": "job_company_name",
    "仕事内容": "job_description",
    "応募条件": "job_condition",
    "英語能力": "job_english_level",
    "勤務時間": "job_working_hours",
    "日本語能力": "job_japanese_level",
    "年収": "job_salary",
    "休日休暇": "job_holiday",
    "契約期間": "job_contract_period",
    "応募条件": "job_working_conditions",
    "休日": "job_holiday",
    "契約期間" :"job_type",
    "最寄り駅": "job_nearest_station",
    "企業について（社風など）": "job_company_business_content",
}
class Recruit(BaseModel):
    job_id : Optional[str] = None
    job_industry : Optional[str] = None
    job_title : Optional[str] = None
    job_company_id : Optional[str] = None
    job_industry : Optional[str] = None
    job_name_title : Optional[str] = None
    job_company_name : Optional[str] = None
    job_description : Optional[str] = None
    job_condition : Optional[str] = None
    job_english_level : Optional[str] = None
    job_japanese_level : Optional[str] = None
    job_salary: Optional[str] = None
    job_salary : Optional[str] = None
    job_contract_period : Optional[str] = None
    job_working_hours : Optional[str] = None
    job_working_conditions : Optional[str] = None
    job_holiday : Optional[str] = None
    job_type : Optional[str] = None
    job_nearest_station : Optional[str] = None
    job_company_business_content : Optional[str] = None
    source_job_url : Optional[str] = None
    job_last_updated : Optional[str] = None
    job_salary : Optional[str] = None
    job_feature : Optional[str] = None
    job_category : Optional[List[str]] = None
    job_korean_level : Optional[str] = None
    job_company_url : Optional[str] = None
    job_company_name_sub: Optional[str] = None
    job_location: Optional[str] = None
    
    
    