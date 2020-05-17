import time
import os
import json
import pandas as pd
import requests, re
from lxml import etree
from bs4 import BeautifulSoup

# 搜尋地區的連結，以及定義連線函數
url = 'https://rent.591.com.tw/home/search/rsList?'  # 搜尋頁網址
ss = requests.session()

# header以及postdata
search_page_headers_str = '''Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,zh;q=0.6,ja;q=0.5
Connection: keep-alive
Cookie: urlJumpIp=1; urlJumpIpByTxt=%E5%8F%B0%E5%8C%97%E5%B8%82; T591_TOKEN=0kr22j6oui0pilarous95eddn6; _ga=GA1.3.1378728357.1587207907; _ga=GA1.4.1378728357.1587207907; tw591__privacy_agree=0; user_index_role=1; __auc=4cce32961718d36cb8993fb5be4; _fbp=fb.2.1587212111380.2098850361; user_browse_recent=a%3A5%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229113523%22%3B%7Di%3A1%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229004419%22%3B%7Di%3A2%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229015948%22%3B%7Di%3A3%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229088532%22%3B%7Di%3A4%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229082564%22%3B%7D%7D; ba_cid=a%3A5%3A%7Bs%3A6%3A%22ba_cid%22%3Bs%3A32%3A%22083b4149f837b886f539b6f64c0578d5%22%3Bs%3A7%3A%22page_ex%22%3Bs%3A48%3A%22https%3A%2F%2Frent.591.com.tw%2Frent-detail-9004419.html%22%3Bs%3A4%3A%22page%22%3Bs%3A48%3A%22https%3A%2F%2Frent.591.com.tw%2Frent-detail-9113523.html%22%3Bs%3A7%3A%22time_ex%22%3Bi%3A1587212227%3Bs%3A4%3A%22time%22%3Bi%3A1587212301%3B%7D; webp=1; PHPSESSID=s7q0lqcjf49akk2d2dcv5a3693; c10f3143a018a0513ebe1e8d27b5391c=1; _gid=GA1.3.898968881.1589432285; _gat=1; _gid=GA1.4.898968881.1589432285; _dc_gtm_UA-97423186-1=1; _gat_UA-97423186-1=1; XSRF-TOKEN=eyJpdiI6IlRRaE9Dd1NORWw0Y2k1WUliaFV5R3c9PSIsInZhbHVlIjoiNGR1NDZOV2djQTNYdDNGeloxRXhZNXp1elNNaTlUQk5MV1wvT2M2Tk92RlMyaXRSeDBtUmM4c2RYeWlGXC90RVR2UVczRnpQZFIwR1o5NTMzMVV2enFhdz09IiwibWFjIjoiMmI4OWNhNjc4ZmQ0OTdlNWEyY2ExNjQ1NDNmYmU3YTJjYWJjN2Y3YzZiYzE0ZjY4OTM5YzlhN2UyMTYyZThkNyJ9; new_rent_list_kind_test=0; 591_new_session=eyJpdiI6Ik92QlNCbXN6ekJja0s4czRIWFRcLzh3PT0iLCJ2YWx1ZSI6InVcL29DdVwvdWhBeFAxanc1K2UwdGVhMEw1cERZQkt0TFhyVmtjY0RkdjkwQXZKcGs4aWlGV2xPZFlkOCtxdUlaZUlrYVV2XC9XWGhXRVVhU3IwMWxZOFVBPT0iLCJtYWMiOiJlMTI1N2RiYjBhZDJmZjM1MzVlOWVhMTIxNjE2NzM3NjdhODE4OWRhZjk5NmY4ZWRiYmQ5YzRlY2Q0OWMyMTY2In0%3D
Host: rent.591.com.tw
Referer: https://rent.591.com.tw/?kind=0&region=1
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36
X-CSRF-TOKEN: nMTVqcW1FW7iQln1MhGimmRTds3xKU10Hc2L5gac
X-Requested-With: XMLHttpRequest'''


taipei_parameters_str_P1 ='''is_new_list: 1
type: 1
kind: 0
searchtype: 1
region: 1'''



# 初步整理，去空格留下list
def list_strip(ori_list):
    for ll, content in enumerate(ori_list):
        ori_list[ll] = content.strip()
    ori_list = list(filter(None, ori_list))
    return ori_list

# 做字典
def data_dict(data):  # headers 轉換dict
    _dict = {}
    for row in data.split('\n'):
        _dict[row.split(': ')[0]] = row.split(': ')[1]
    return _dict


# 輸入parameters獲取相對應頁面的租屋網址列表

headers = data_dict(search_page_headers_str)
parameters = data_dict(taipei_parameters_str_P1)

res = ss.get(url, headers=headers, data=parameters)
#print(res)
print(res.text)
js = json.loads(res.text)
total_house = js['records']
totalRows = total_house.replace(',', '')
print(totalRows)

rentdata = js['data']['data']
for i in range(30):
    id = rentdata[i]['id']
    print(id)  #id物件
    house_url = 'https://rent.591.com.tw/rent-detail-{}.html'.format(id)
    print(house_url)   #page的網址

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    headers = {'User-Agent': user_agent}

    res_content = ss.get(house_url, headers=headers)
    #print(res_content.text)
    soup = BeautifulSoup(res_content.text, 'html.parser')
    tree_content = etree.HTML(res_content.text)
    renter = tree_content.xpath('//*[@id="main"]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/div/i/text()')
    print(renter)   #出租者
    landlord = tree_content.xpath('//*[@id="main"]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/div/text()')
    landlord2 = list_strip(landlord)
    print(landlord2)    #出租者身分
    phone = tree_content.xpath('//span[@class="dialPhoneNum"]/@data-value')
    print(phone)     #連絡電話

    ### 出租資料的預處理 ###
    rent_info = tree_content.xpath('//*[@id="main"]/div[3]/div[2]/div[2]/div[1]/ul/li/text()')
    #print(rent_info)
    rent_info_join = ''.join(rent_info)
    rent_info_str = rent_info_join.replace('\xa0', '')   #去空白
    rent_type = re.findall(r'型態:(\w+)現況', rent_info_str)
    if re.findall(r'現況:(\w+)社區', rent_info_str):
        rent_situation = re.findall(r'現況:(\w+)社區', rent_info_str)
    else:
        rent_situation = re.findall(r'現況:(\w+)', rent_info_str)
    print(rent_type)   #型態
    print(rent_situation)   #現況

    ### 出租資料的預處理 -->性別要求 ###
    rent_detail = tree_content.xpath('//li[@class="clearfix"]/div[2]/em/text()')
    #print(rent_detail)
    rent_detail_join = ''.join(rent_detail)
    #print(rent_detail_join)
    if re.findall(r'男女生皆可', rent_detail_join):
        gender = re.findall(r'男女生皆可', rent_detail_join)
    elif re.findall(r'女生', rent_detail_join):
        gender = re.findall(r'女生', rent_detail_join)
    elif re.findall(r'男生', rent_detail_join):
        gender = re.findall(r'男生', rent_detail_join)
    else:
        gender = '沒有提供'
    print(gender)  #性別要求



















