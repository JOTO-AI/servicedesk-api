from pydantic import BaseModel

class RequestModel(BaseModel):
    customer_name: str
    description: str
    priority_name: str
    contact_info: str

class CustomerModel(BaseModel):
    name: str
    id: str

class TechnicianModel(BaseModel):
    name: str
    id: str = "5"

class PriorityModel(BaseModel):
    name: str
    id: str
    color: str | None = None  # 可选字段

    class Config:
        from_attributes = True  # 允许从ORM模型创建

