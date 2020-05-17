import os

channel = input('請輸入地區名稱(taipei or newpei):')
file_list = os.listdir('./combine_save/'+ channel )
for each_file in file_list:
    each_file_path = './combine_save/clear_data/' + each_file
    with open(each_file_path, 'r', encoding='utf-8') as f:  # 讀檔~
        file_content = f.read()
        rent_house_save = str(file_content) + '\n'
        #filename = './' + channel +'_rents.json'
        filename = './all_rents.json'
        file = open(filename, 'a+', encoding="utf-8")
        file.write(rent_house_save)
        file.close()




