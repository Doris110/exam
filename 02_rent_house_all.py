import time
import os
import json
import pandas as pd
import requests, re
from lxml import etree
from bs4 import BeautifulSoup

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


# 定義連線函數
ss = requests.session()

# header以及postdata
search_page_headers_str = '''Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,zh;q=0.6,ja;q=0.5
Connection: keep-alive
Cookie: T591_TOKEN=pcvg5f5snequ63hkkhqp6g0ba1; c10f3143a018a0513ebe1e8d27b5391c=1; _ga=GA1.3.113481885.1589526153; _gid=GA1.3.987112618.1589526153; _ga=GA1.4.113481885.1589526153; _gid=GA1.4.987112618.1589526153; _fbp=fb.2.1589526154031.889031654; tw591__privacy_agree=0; urlJumpIp=3; urlJumpIpByTxt=%E6%96%B0%E5%8C%97%E5%B8%82; new_rent_list_kind_test=0; user_index_role=1; __auc=b34d595b172172a7b63f3769f6e; user_browse_recent=a%3A2%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229150637%22%3B%7Di%3A1%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%223032970%22%3B%7D%7D; ba_cid=a%3A5%3A%7Bs%3A6%3A%22ba_cid%22%3Bs%3A32%3A%22d0e6690ffeb1e4b6e9fbc3519ba70e5b%22%3Bs%3A7%3A%22page_ex%22%3Bs%3A48%3A%22https%3A%2F%2Frent.591.com.tw%2Frent-detail-3032970.html%22%3Bs%3A4%3A%22page%22%3Bs%3A48%3A%22https%3A%2F%2Frent.591.com.tw%2Frent-detail-9150637.html%22%3Bs%3A7%3A%22time_ex%22%3Bi%3A1589526559%3Bs%3A4%3A%22time%22%3Bi%3A1589526645%3B%7D; webp=1; PHPSESSID=2ku9vhj2480esu6cog0hrkhcs5; _gat=1; _dc_gtm_UA-97423186-1=1; XSRF-TOKEN=eyJpdiI6ImZ6R0YyeTBaMUc0SzRSWUdxZE9DdkE9PSIsInZhbHVlIjoicXJhMFRjaVNCZUdaTXdRNGFxSVFsNytWajhXaFpuZGpZQ2l6NFlSeWdMemhxY1QxNlhIM3VWMUZ1VjdLK000Z2ZweGpkZ2krMmVOMjRoaFFjcmRyREE9PSIsIm1hYyI6IjE5MTU1NTlkYmFmNDY3ZGUzY2QwYTQxOWM4NzE4ZmMxMDYzY2RmODk4NTQ5NDM2NjZiNTkyMmMyZmE4NmJjOTMifQ%3D%3D; _gat_UA-97423186-1=1; 591_new_session=eyJpdiI6Ik5LV3RTeVwvYmp2QWZZM3EybG9OeVwvZz09IiwidmFsdWUiOiJQalFNbVpcL1pqREMwRDVMdHVsT1E1U1pwbjZ3NnlSNHhLcFN6Wk1xcEo2OVN0XC96R2Rna3dVMEVKak5iWmwxeElcL2E3S21FSjlnS2pBRFhEQ3hyTGNwUT09IiwibWFjIjoiZjNhYmVhMmVmNWIxNWRhMTFjZDhmMzhiOGM2MWZlNmFhOGQwYTk0ODFjM2Y0ZTc1MTI4ZGMyMTExMmNiYTUzNSJ9
Host: rent.591.com.tw
Referer: https://rent.591.com.tw/?kind=0&region=3
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36
X-CSRF-TOKEN: o7sHLDpZViv1u93RzO6faZimxOrvaE3NNnXlAvV4
X-Requested-With: XMLHttpRequest'''


headers = data_dict(search_page_headers_str)
next_page = 1 # while的開關，假如這個頁面已經沒有連結(跑到最後一頁又繼續翻頁)就會把它切換成0，然後停止while迴圈
firstRow = 9150# 起始搜尋位置

while next_page == 1:
    url = 'https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=3&firstRow={}'.format(firstRow) # 搜尋頁網址
    print(url)
    res = ss.get(url, headers=headers)
    print(res)
    print(res.text)
    js = json.loads(res.text)
    rentData = js['data']['data']
    print(len(rentData))
    print('正在爬取第{}頁'.format(round(firstRow / 30 + 1)))
    if rentData:
        for i in range(len(rentData)):
            id = rentData[i]['id']
            #print(id)  #id物件
            house_url = 'https://rent.591.com.tw/rent-detail-{}.html'.format(id)
            print(house_url)  # page的網址

            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            headers_c = {'User-Agent': user_agent}

            res_content = ss.get(house_url, headers=headers_c)
            # print(res_content.text)
            soup = BeautifulSoup(res_content.text, 'html.parser')
            tree_content = etree.HTML(res_content.text)
            try :
                renter = tree_content.xpath('//*[@id="main"]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/div/i/text()')[0]
                print(renter)  # 出租者
                landlord = tree_content.xpath('//*[@id="main"]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/div/text()')
                landlord2 = list_strip(landlord)[0]
                print(landlord2)  # 出租者身分

                if tree_content.xpath('//span[@class="dialPhoneNum"]/@data-value'):
                    phone = tree_content.xpath('//span[@class="dialPhoneNum"]/@data-value')[0]
                elif tree_content.xpath('//*[@id="hid_tel"]/@value'):
                    phone = tree_content.xpath('//*[@id="hid_tel"]/@value')[0]
                elif tree_content.xpath('//*[@id="main"]//div[@class="hidtel"]/text()'):
                    phone = tree_content.xpath('//*[@id="main"]//div[@class="hidtel"]/text()')[0]
                else:
                    phone = ''
                print(phone)  # 連絡電話

                ### 出租資料的預處理 ###
                rent_info = tree_content.xpath('//*[@id="main"]/div[3]/div[2]/div[2]/div[1]/ul/li/text()')
                # print(rent_info)
                rent_info_join = ''.join(rent_info)
                rent_info_str = rent_info_join.replace('\xa0', '')  # 去空白
                if re.findall(r'型態:(\w+)現況', rent_info_str):
                    rent_type = re.findall(r'型態:(\w+)現況', rent_info_str)[0]
                elif re.findall(r'型態:(\w+)社區', rent_info_str):
                    rent_type = re.findall(r'型態:(\w+)社區', rent_info_str)[0]
                else:
                    rent_type = ''
                if re.findall(r'現況:(\w+)社區', rent_info_str):
                    rent_situation = re.findall(r'現況:(\w+)社區', rent_info_str)[0]
                elif re.findall(r'現況:(\w+)', rent_info_str):
                    rent_situation = re.findall(r'現況:(\w+)', rent_info_str)[0]
                else:
                    rent_situation = ''
                print(rent_type)  # 型態
                print(rent_situation)  # 現況

                ### 出租資料的預處理 -->性別要求 ###
                rent_detail = tree_content.xpath('//li[@class="clearfix"]/div[2]/em/text()')
                # print(rent_detail)
                rent_detail_join = ''.join(rent_detail)
                # print(rent_detail_join)
                if re.findall(r'男女生皆可', rent_detail_join):
                    gender = re.findall(r'男女生皆可', rent_detail_join)[0]
                elif re.findall(r'女生', rent_detail_join):
                    gender = re.findall(r'女生', rent_detail_join)[0]
                elif re.findall(r'男生', rent_detail_join):
                    gender = re.findall(r'男生', rent_detail_join)[0]
                else:
                    gender = ''
                print(gender)  # 性別要求


                rent_house = dict(出租者=renter, 出租者身分=landlord2, 連絡電話=phone, 型態=rent_type, 現況=rent_situation, 性別要求=gender)
                print(rent_house)

                # -----存檔----------
                rent_house_save = str(rent_house) + '\n'
                filename = './newpei007.json'
                file = open(filename, 'a+', encoding="utf-8")
                file.write(rent_house_save)
                file.close()
                time.sleep(1)
            except:
                print('物件不存在，可能已關閉或者被刪除')
                pass



        firstRow += 30
    else:
        next_page = 0



if __name__ == "__main__":
    start = time.time()
    print('Complete!!!!!!!!!!')
    end = time.time()
    spend = end - start
    hour = spend // 3600
    minu = (spend - 3600 * hour) // 60
    sec = spend - 3600 * hour - 60 * minu
    print(f'一共花費{hour}小時{minu}分鐘{sec}秒')



