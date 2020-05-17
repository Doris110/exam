import os, json
import pandas as pd
from pymongo import MongoClient
import pymongo


myclient = pymongo.MongoClient("mongodb://34.97.198.241:27017/")

channel = input('請輸入檔案名稱(taipei,newpei or all):')

mydb = myclient["clear_data"]
mycol1 = mydb["taipei"]
mycol2 = mydb["newpei"]
mycol3 = mydb["all_info"]

house_data = pd.DataFrame()
filename1 = './taipei_rents.json'
filename2 = './newpei_rents.json'
filename = './' + channel + '_rents.json'


with open(filename, 'r', encoding='utf-8-sig') as f:
    for i, eachhouse in enumerate(f.readlines()):
        eachhouse = eval(eachhouse)
        df = pd.DataFrame(
            data=[{'region': eachhouse['region'],
                   'renter': eachhouse['renter'],
                   'landlord': eachhouse['landlord'],
                   'phone': eachhouse['phone'],
                   'rent_type': eachhouse['rent_type'],
                   'situation': eachhouse['situation'],
                   'gender': eachhouse['gender'],
                   }],
            columns=['region','renter', 'landlord', 'phone','rent_type','situation','gender'])

        house_data = house_data.append(df, ignore_index=True)
        print(house_data)

    # duplicated_df = pd.DataFrame(house_data)
    #
    # # 去除重複觀測值
    # house_cleardata = duplicated_df.drop_duplicates()
    # house_all = house_cleardata.reset_index(drop=True)
    # print(house_all)
    # print(len(house_all))


    for j in range(len(house_data['renter'])):
        dict = {
                "region": house_data['region'][j],
                "renter": house_data['renter'][j],
                "landlord": house_data['landlord'][j],
                "phone": house_data['phone'][j],
                "rent_type": house_data['rent_type'][j],
                "situation": house_data['situation'][j],
                "gender": house_data['gender'][j]
                }
        print(dict)
        x = mycol3.insert_one(dict)
        print(x)





