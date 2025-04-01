import requests
import json
from ..config import settings
from ..utils.helpers import parse_html_tables, get_current_timestamp
from ..models.schemas import CustomerModel, TechnicianModel, PriorityModel

class ServiceDeskService:
    def get_customer(self, customer_name: str) -> CustomerModel:
        url = settings.base_url + "requests/udf_fields/udf_pick_306"
        headers = {"authtoken": settings.authtoken}
        response = requests.get(url, headers=headers, verify=False)
        print(f"API Response: {response.json()}")  # 添加调试信息
        
        for item in response.json()["udf_pick_306"]:
            if customer_name in item["name"]:
                return CustomerModel(name=item["name"], id=item["id"])
        return None

    def get_technician(self, customer_name: str) -> TechnicianModel:
        url = settings.base_url + "announcements"
        headers = {"authtoken": settings.authtoken}
        response = requests.get(url, headers=headers, verify=False)
        data = response.json()
        
        for announcement in data['announcements']:
            if announcement['title'] == "客户维保服务 L1/L2 责任分配":
                engineer = parse_html_tables(announcement['content'], customer_name)
                if engineer:
                    return TechnicianModel(name=engineer)
        
        return TechnicianModel(name="administrator", id="5")
    
    def get_priority(self, priority_name: str) -> PriorityModel:
        url = settings.base_url + "requests/priority"
        headers = {"authtoken": settings.authtoken}
        response = requests.get(url, headers=headers, verify=False)
        data = response.json()
        for priority in data['priority']:
            if priority['name'] == priority_name:
                return PriorityModel(name=priority['name'], id=priority['id'])

    def create_request(self, customer_name: str, description: str, priority_name: str, contact_info: str):
        url = settings.base_url + "requests"
        headers = {"authtoken": settings.authtoken}
        
        # 获取客户信息
        customer = self.get_customer(customer_name)
        if not customer:
            raise ValueError(f"Customer not found: {customer_name}")
        
        # 获取技术员信息
        technician = self.get_technician(customer_name)
        timestamp = get_current_timestamp()
        priority = self.get_priority(priority_name)
        
        input_data = {
            "request": {
                "subject": description,  # 使用description作为subject
                "description": f"<div><b>问题现象：</b><br /></div><div>{description}</div>",
                "request_type": {"name": "服务请求", "id": "2"},
                "template": {
                    "is_service_template": False,
                    "service_category": None,
                    "name": "智能运维服务模板",
                    "id": "901"
                },
                "requester": {"name": "Support.Ai", "id": "901"},
                "status": {"name": "Open", "id": "2"},
                "group": {"name": "IT 技术运维组", "id": "4"},
                "priority": {"name": priority.name, "id": priority.id},
                "technician": {"name": technician.name},
                "udf_fields": {
                    "udf_pick_306": {
                        "name": customer.name,
                        "id": customer.id
                    },
                    "udf_sline_307": contact_info,  # 添加联系方式
                    "udf_date_156": timestamp
                }
            }
        }
        
        data = {'input_data': json.dumps(input_data)}
        response = requests.post(url, headers=headers, data=data, verify=False)
        response_data = response.json()
        
        # 确保返回的是字典而不是模型对象
        return {
            "status": "success" if response.status_code in [200, 201] else "error",
            "data": response_data
        } 