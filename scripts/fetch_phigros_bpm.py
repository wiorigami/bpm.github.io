import requests
from bs4 import BeautifulSoup
import json

def fetch_phigros_bpm():
    url = 'https://phigros.fandom.com/zh/wiki/%E6%9B%B2%E7%9B%AE%E5%88%97%E8%A1%A8'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    bpm_list = []
    # 根据页面结构定位包含曲目信息的表格
    tables = soup.find_all('table', {'class': 'wikitable'})
    for table in tables:
        rows = table.find_all('tr')[1:]  # 跳过表头
        for row in rows:
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 2:
                name = cols[0].get_text(strip=True)
                bpm_text = cols[1].get_text(strip=True)
                try:
                    bpm = float(bpm_text)
                    bpm_list.append({'name': name, 'bpm': bpm})
                except ValueError:
                    continue  # 跳过无法解析的 BPM 值

    with open('assets/bpm_phigros/phigros_bpm.json', 'w', encoding='utf-8') as f:
        json.dump(bpm_list, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    fetch_phigros_bpm()
