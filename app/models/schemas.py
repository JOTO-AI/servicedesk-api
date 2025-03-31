from pydantic import BaseModel

class RequestModel(BaseModel):
    customer_name: str
    description: str
    contact_info: str

class CustomerModel(BaseModel):
    name: str
    id: str

class TechnicianModel(BaseModel):
    name: str