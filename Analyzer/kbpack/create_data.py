# 금리 라벨링 부분, 음수 Day도 사용 가능 기본값 Date_Range +28일, Limit 0.03
def rate_label(datas, name, dr = 28, rl = 0.03):
    temp = []
    # 금리 부분 Column rate로 통일해야 함, 라벨 부분 Column ud로 통일
    if dr < 0:
        for i in range(-dr, len(datas)):
            rate_change = float(datas[name][i]) - float(datas[name][i+dr])
            if rate_change >= datas[name][i] * rl:
                temp.append(1)
            elif rate_change <= -datas[name][i] * rl:
                temp.append(0)
            else:
                temp.append(None)
        new_data = datas.iloc[-dr:].reset_index()
    else:
        for i in range(len(datas)-dr):
            rate_change = float(datas[name][i+dr]) - float(datas[name][i])
            if rate_change >= datas[name][i] * rl:
                temp.append(1)
            elif rate_change <= -datas[name][i] * rl:
                temp.append(0)
            else:
                temp.append(None)
        new_data = datas.iloc[:-dr].reset_index()
    new_data['ud'] = temp
    new_data.dropna(inplace=True)
    new_data['date'] = list(map(lambda i : i.date(), new_data['date']))

    # 제이슨 파일로 저장 필요 시
    new_data[['date',name,'ud']].to_json('/home/lab10/JJC/KB_AI_Challenge/Analyzer/data/label/final/{}_ud.json'.format(name))
    # return new_data.set_index('date')

import pandas as pd
import os
import re

def search(dirname):
    filenames = os.listdir(dirname)
    fl = []
    for filename in filenames:
        if '.json' in filename:
            fl.append(os.path.join(dirname, filename))
    return fl

# fl = search('/home/lab10/JJC/KB_AI_Challenge/Analyzer/data/label')
# for f in fl:
#     print(f)
#     print(re.search('(?<=label\/).*(?=\_ud\.json)', f).group())
#     rate_label(pd.read_json(f), re.search('(?<=label\/).*(?=\_ud\.json)', f).group())
    
def create_folder(folder_name):
    
    fol_dir = '/home/lab10/JJC/KB_AI_Challenge/Analyzer/finance_data/' + folder_name
    try:
        if not os.path.exists(fol_dir):
            os.makedirs(fol_dir)
    except OSError:
        print('Error: Creating Directory' + fol_dir)

    return fol_dir

import datetime

temp_df = pd.read_csv('/home/lab10/JJC/KB_AI_Challenge/Analyzer/data/news/titles/focus_title.txt', sep='\t')
temp_df['date'] = list(map(lambda i : datetime.datetime.strptime(i, '%Y-%m-%d'), temp_df['date']))
temp_df.set_index('date', inplace=True)
fl = search('/home/lab10/JJC/KB_AI_Challenge/Analyzer/data/label/final')
for f in fl:
    this_name = re.search('(?<=final\/).*(?=\_ud\.json)', f).group()
    file_path = create_folder(this_name+'_data')
    # print(type(temp_df.index[0]))
    # break
    temp_df['ud'] = pd.read_json(f).set_index('date')['ud']
    temp_df['ud'] = list(map(int, temp_df['ud']))
    temp_df[temp_df.index < datetime.datetime(2019,1,1)].dropna().to_csv(file_path+'/finance_trian.txt', sep='\t')
    temp_df[temp_df.index > datetime.datetime(2018,12,31)].dropna().to_csv(file_path+'/finance_test.txt', sep='\t')
