# 목표 데이터 수치화 (Positive, Negative, Score)

import os
import sys
sys.path.insert(0, os.path.abspath('../'))

from transformers import pipeline, AutoModelForSequenceClassification
from kbpack.tokenization_kbalbert import KbAlbertCharTokenizer

kb_albert_model_path = '/home/lab10/JJC/KB_AI_Challenge/Analyzer/model'
# 학습한 모델 경로
model_output_path = '/home/lab10/JJC/KB_AI_Challenge/Analyzer/finance_outputs'

model = AutoModelForSequenceClassification.from_pretrained(model_output_path)
tokenizer = KbAlbertCharTokenizer.from_pretrained(kb_albert_model_path)

finance_classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer, framework='pt')

# Target Text
import pandas as pd
target_data = pd.read_csv('/home/lab10/JJC/KB_AI_Challenge/Analyzer/finance_data/finance_test.txt', sep='\t')
# reviews = ['이 영화 최악이었어!',
#            '볼거리가 많은 내 인생 영화 ㅎㅎ']
import datetime
import pickle
import time
date_length = datetime.date(2020,12,31) - datetime.date(2018,12,31)
for i in range(date_length.days):
    now_day = datetime.date(2019,1,1) + datetime.timedelta(i)
    # print(now_day)
    datas = list(target_data[target_data['date'] == now_day.strftime('%Y-%m-%d')]['text'])
    if not datas:
        continue
    try:
        result = finance_classifier(datas)
        final_result = pd.DataFrame(result)
        final_result['date'] = now_day
        final_result.to_csv('/home/lab10/JJC/KB_AI_Challenge/Analyzer/result/final/{}.txt'.format(i))

    except:
        pass
    
# target_data['result'] = results
# target_data[['date', 'text', 'result']].to_csv('/home/lab10/JJC/KB_AI_Challenge/Analyzer/result/result.txt')
# for result in results:
#     print(f"label: {result['label']}, with score: {round(result['score'], 4)}")

