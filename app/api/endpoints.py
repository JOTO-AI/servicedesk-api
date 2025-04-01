from fastapi import APIRouter, HTTPException
from ..models.schemas import RequestModel
from ..core.service import ServiceDeskService

router = APIRouter()
service = ServiceDeskService()

@router.post("/create_request")
async def create_request(request_data: RequestModel):
    try:
        response = service.create_request(
            request_data.customer_name,
            request_data.description,
            request_data.priority_name,
            request_data.contact_info
        )
        
        # response 是一个字典，直接检查 status
        if response["status"] == "success":
            return {
                "status": "success",
                "message": "工单创建成功",
                "data": response["data"]
            }
        else:
            # 从响应中获取具体错误信息
            error_message = response["data"].get('response_status', {}).get('messages', [])
            if error_message:
                error_detail = error_message[0].get('message', '未知错误')
            else:
                error_detail = '服务器返回错误'
                
            raise HTTPException(
                status_code=400,  # 使用400作为默认错误状态码
                detail=error_detail
            )
            
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 