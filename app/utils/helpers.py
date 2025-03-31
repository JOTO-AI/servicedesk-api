from datetime import datetime
from bs4 import BeautifulSoup

def parse_html_tables(html_content: str, customer_name: str):
    # 解析html内容,获取一线工程师
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    
    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:
            cells = row.find_all('td')
            if len(cells) >= 2:
                client = cells[0].get_text(strip=True)
                engineer = cells[1].get_text(strip=True)
                if customer_name in client:
                    return engineer
    return None

def get_current_timestamp():
    # 获取当前时间,并格式化
    current_time = datetime.now()
    return {
        "display_value": current_time.strftime("%b %d, %Y %I:%M %p"),
        "value": str(int(current_time.timestamp() * 1000))
    } 