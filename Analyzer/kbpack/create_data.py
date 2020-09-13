import datetime
# 금리 라벨링 부분, 음수 Day도 사용 가능 기본값 Date_Range +28일, Limit 0.03
def rate_label(datas, name, dr = 28, rl = 0.03):
    temp = []
    datas['date'] = list(map(lambda i : datetime.datetime.strptime(i, '%Y-%m-%d'), datas['date']))
    # 금리 부분 Column rate로 통일해야 함, 라벨 부분 Column ud로 통일
    if dr < 0:
        for i in range(-dr, len(datas)):
            rate_change = float(datas[name][i]) - float(datas[name][i+dr])
            if rate_change >= rl:
                temp.append(1)
            elif rate_change <= - rl:
                temp.append(0)
            else:
                temp.append(None)
        new_data = datas.iloc[-dr:].reset_index()
    else:
        for i in range(len(datas)-dr):
            rate_change = float(datas[name][i+dr]) - float(datas[name][i])
            if rate_change >= rl:
                temp.append(2)
            elif rate_change <= -rl:
                temp.append(0)
            else:
                temp.append(1)
        new_data = datas.iloc[:-dr].reset_index()
    new_data['ud'] = temp
    print(new_data.head())
    new_data.dropna(inplace=True)
    new_data['date'] = list(map(lambda i : i.date(), new_data['date']))
    new_data['ud'] = list(map(int, new_data['ud']))

    # 제이슨 파일로 저장 필요 시
    new_data[['date',name,'ud']].to_json('/home/lab10/JJC/KB_AI_Challenge/Analyzer/data/label/final/{}{}_ud.json'.format(name,dr))
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

# 라벨 붙이기
# fl = search('/home/lab10/JJC/KB_AI_Challenge/Analyzer/data/label')
# for f in fl:
#     print(f)
#     print(re.search('(?<=label\/).*(?=\_ud\.json)', f).group())
for i in range(7, 8):
    rate_label(pd.read_csv('/home/lab10/JJC/KB_AI_Challenge/Analyzer/hottae_data/vix.csv'), name='vix', dr= i, rl=0.01)

    
def create_folder(folder_name):
    
    fol_dir = '/home/lab10/JJC/KB_AI_Challenge/Analyzer/hottae_data/' + folder_name
    try:
        if not os.path.exists(fol_dir):
            os.makedirs(fol_dir)
    except OSError:
        print('Error: Creating Directory' + fol_dir)

    return fol_dir






# temp_df.set_index('date', inplace=True)
fl = search('/home/lab10/JJC/KB_AI_Challenge/Analyzer/data/label/final')
for f in fl:
    if 'vix7_ud' not in f:
        continue
    this_name = re.search('(?<=final\/).*(?=\_ud\.json)', f).group()

    train_df = pd.read_csv('/home/lab10/JJC/KB_AI_Challenge/Analyzer/hottae_data/[금리]_first2sent_train.txt', sep='\t')
    test_df = pd.read_csv('/home/lab10/JJC/KB_AI_Challenge/Analyzer/hottae_data/[금리]_first2sent_test.txt', sep='\t')
    train_df['date'] = list(map(lambda i : datetime.datetime.strptime(i, '%Y-%m-%d'), train_df['date']))
    test_df['date'] = list(map(lambda i : datetime.datetime.strptime(i, '%Y-%m-%d'), test_df['date']))
    train_df.set_index('date', inplace=True)
    test_df.set_index('date', inplace=True)

    label_df = pd.read_json(f)
    # label_df['date'] = list(map(lambda i : datetime.datetime.strptime(i, '%Y-%m-%d'), label_df['date']))

    # print(label_df.head())
    label_df.set_index('date', inplace=True)
    train_df['ud'] = label_df['ud']
    test_df['ud'] = label_df['ud']
    train_df.dropna(inplace=True)
    test_df.dropna(inplace=True)
    train_df['ud'] = list(map(int, train_df['ud']))
    test_df['ud'] = list(map(int, test_df['ud']))
    file_path = create_folder('{}_data'.format(this_name))
    train_df[['text','ud']].to_csv('{}/finance_train.txt'.format(file_path), sep='\t')
    test_df[['text','ud']].to_csv('{}/finance_test.txt'.format(file_path), sep='\t')

    # temp_df['ud'] = pd.read_json(f).set_index('date')['ud']
    # temp_df.dropna(inplace=True)
    # temp_df['ud'] = list(map(int, temp_df['ud']))
    # temp_df[temp_df.index < datetime.datetime(2019,1,1)].dropna().to_csv(file_path+'/finance_trian.txt', sep='\t')
    # temp_df[temp_df.index > datetime.datetime(2018,12,31)].dropna().to_csv(file_path+'/finance_test.txt', sep='\t')
