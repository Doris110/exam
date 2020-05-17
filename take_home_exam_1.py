import os
import requests,re
import pandas as pd

ss = requests.session()

headers = '''Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,zh;q=0.6,ja;q=0.5
Connection: keep-alive
Cookie: _ga=GA1.3.275091886.1586772600; _gid=GA1.3.2020760835.1586772600; JSESSIONID=A1C153B23F997FB5E8985D6FED7E4C99; _gat=1
Host: plvr.land.moi.gov.tw
Referer: https://plvr.land.moi.gov.tw/DownloadOpenData
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'''


# 做字典
def data_dict(data):  # headers 轉換dict
    _dict = {}
    for row in data.split('\n'):
        _dict[row.split(': ')[0]] = row.split(': ')[1]
    return _dict


download_path = './download'
if not os.path.exists(download_path):
    os.mkdir(download_path)

fileName = ['a','f','h','b','e']  #[臺北,新北,桃園,臺中,高雄]
for i,f in enumerate(fileName):
    main_url = 'https://plvr.land.moi.gov.tw//Download?fileName={}_lvr_land_a.csv'.format(fileName[i])
    print(main_url)
    main_headers = data_dict(headers)
    res = ss.get(main_url, headers=main_headers)
    #print(res)
    #print(res.text) csv的內容
    df = pd.read_csv(main_url)
    # 將檔案抓下來
    df.to_csv('./download/{}_lvr_land_a.csv'.format(fileName[i]), encoding='utf-8-sig', index=False)


# 讀取抓下來的檔案
pf_a = pd.read_csv("download/a_lvr_land_a.csv")
pf_b = pd.read_csv("download/b_lvr_land_a.csv")
pf_e = pd.read_csv("download/e_lvr_land_a.csv")
pf_f = pd.read_csv("download/f_lvr_land_a.csv")
pf_h = pd.read_csv("download/h_lvr_land_a.csv")

df_raw_0 = pd.concat([pf_a,pf_b,pf_e,pf_f,pf_h])  #預設axis=0，在0軸上合併
df_raw_1 = df_raw_0.drop(index=[0])   #去除重複列，英文那列不要
df_all = df_raw_1.reset_index(drop=True)
print(len(df_all))  #data=3,826筆
#df_all.to_csv('./download/all_lvr_land.csv', encoding='utf-8-sig',index=False)


#-------------------filter_a---------------------------------------

filter_0 = df_all['主要用途'] == '住家用'  #顯示True否則False
filter_1 = df_all['建物型態'] == '住宅大樓(11層含以上有電梯)'
filter_2 = df_all['總樓層數'] != '十一層'
filter_3 = df_all['總樓層數'] != '十二層'
filter_a = df_all[(filter_0 & filter_1 & filter_2 & filter_3)]
#print(filter_a)
filter_a.to_csv('./download/filter_a.csv', encoding='utf-8-sig',index=False)


#-------------------filter_b---------------------------------------
# 總件數
cases = len(df_all)
print(df_all.shape)
print('總件數:{:,}'.format(cases))

# 總車位數
df_test = df_all.copy()
data = df_test[['編號','交易筆棟數','總價元','車位總價元']]
data['車位'] = data['交易筆棟數'].str[-1]
data['車位'] = data['車位'].astype('int')
#data.to_csv('./download/filter_b_test.csv', encoding='utf-8-sig',index=False)
cars = data['車位'].sum()
print('總車位數:{:,}'.format(cars))

# 平均總價元
data['總價元'] = data['總價元'].astype('int64')
avg_dollar = round(data['總價元'].mean(),0)
print('平均總價元:{:,}'.format(avg_dollar))


# 平均車位總價元
data['車位總價元'] = data['車位總價元'].astype('int64')
filter_4 = data['車位總價元'] != 0
filter_test = data[(filter_4)]
print(filter_test.shape)
sum_cars_dollar = filter_test['車位總價元'].sum()
sum_cars = filter_test['車位'].sum()
avg_cars = round((sum_cars_dollar/sum_cars),0)
print('平均車位總價元:{:,}'.format(avg_cars))

# 建立dataframe
count = ['總件數','總車位數','平均總價元','平均車位總價元']
result = [cases,cars,avg_dollar,avg_cars]

dict = {"count": count,
        "result": result }

filter_b_df = pd.DataFrame(dict)
filter_b_df.to_csv('./download/filter_b.csv', encoding='utf-8-sig',index=False)






