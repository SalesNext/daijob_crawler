from typing import Optional, List
from pydantic import BaseModel

class Company(BaseModel):
    company_id: Optional[str] = None
    company_name: Optional[str] = None
    company_head_office: Optional[str] = None
    company_country_residence: Optional[str] = None
    company_business_content: Optional[str] = None
    company_industry: Optional[str] = None
    company_address: Optional[str] = None
    company_representative: Optional[str] = None
    company_establish_date: Optional[str] = None
    company_capital: Optional[str] = None
    company_employee_count: Optional[str] = None
    company_description: Optional[str] = None
    company_nearrest_station: Optional[str] = None
    company_hp_url: Optional[str] = None
    company_welfare: Optional[str] = None