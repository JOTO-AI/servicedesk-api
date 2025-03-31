# Service Desk API

自动创建工单的API服务。

## 功能特性
- 自动获取客户信息
- 自动分配技术员
- 创建工单请求

## 安装部署
1. 克隆仓库
```bash
git clone [repository_url]
```

2. 创建环境变量文件
```bash
cp .env.example .env
# 编辑 .env 文件，填入实际配置
```

3. 使用Docker部署
```bash
docker build -t servicedesk-api .
docker run -d --name servicedesk-api -p 8000:8000 -v $(pwd)/.env:/app/.env servicedesk-api
```

## API文档
启动服务后访问: http://localhost:8000/docs

## 使用示例
```bash
curl -X POST "http://localhost:8000/api/create_request" \
     -H "Content-Type: application/json" \
     -d '{
           "customer_name": "客户名称",
           "description": "问题描述",
           "contact_info": "联系方式"
         }'
```