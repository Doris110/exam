import os, json
import pandas as pd


channel = input('請輸入地區名稱(taipei or newpei):')
house_data = pd.DataFrame()
filename = './' + channel +'_rents.json'


with open(filename, 'r', encoding='utf-8-sig') as f:
    for i, eachhouse in enumerate(f.readlines()):
        eachhouse = eval(eachhouse)
        df = pd.DataFrame(
            data=[{'地區': '新北市',
                   '出租者': eachhouse['出租者'],
                   '出租者身分': eachhouse['出租者身分'],
                   '連絡電話': eachhouse['連絡電話'],
                   '型態': eachhouse['型態'],
                   '現況': eachhouse['現況'],
                   '性別要求': eachhouse['性別要求'],
                   }],
            columns=['地區','出租者', '出租者身分', '連絡電話','型態','現況','性別要求'])

        house_data = house_data.append(df, ignore_index=True)
        print(house_data)

duplicated_df = pd.DataFrame(house_data)


# 去除重複觀測值
house_cleardata = duplicated_df.drop_duplicates()
house_all = house_cleardata.reset_index(drop=True)
print(house_all)
print(len(house_all))

for j in range(len(house_all['出租者'])):
    dict = {
        "region": house_all['地區'][j],
        "renter": house_all['出租者'][j],
        "landlord": house_all['出租者身分'][j],
        "phone": house_all['連絡電話'][j],
        "rent_type": house_all['型態'][j],
        "situation": house_all['現況'][j],
        "gender": house_all['性別要求'][j]
    }

    print(dict)

    # -----存檔----------
    house_all_save = str(dict) + '\n'
    newfile = './combine_save/' + channel + '_newrents.json'
    file = open(newfile, 'a+', encoding="utf-8")
    file.write(house_all_save)
    file.close()
