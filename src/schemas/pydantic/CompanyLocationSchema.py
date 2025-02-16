from pydantic import BaseModel

class CompanySchema(BaseModel):
    company_id : int
    location_id : int