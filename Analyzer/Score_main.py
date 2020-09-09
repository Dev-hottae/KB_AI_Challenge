# 목표 데이터 수치화 (Positive, Negative, Score)

import os
import sys
sys.path.insert(0, os.path.abspath('../'))

from transformers import pipeline, AutoModelForSequenceClassification
from kbpack.tokenization_kbalbert import KbAlbertCharTokenizer

kb_albert_model_path = '/home/lab10/JJC/KB_AI_Challenge/Analyzer/model'
# 학습한 모델 경로
model_output_path = '/home/lab10/JJC/KB_AI_Challenge/Analyzer/model_output'

model = AutoModelForSequenceClassification.from_pretrained(model_output_path)
tokenizer = KbAlbertCharTokenizer.from_pretrained(kb_albert_model_path)

finance_classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer, framework='pt')

# Target Text
target_data = ['texts']
# reviews = ['이 영화 최악이었어!',
#            '볼거리가 많은 내 인생 영화 ㅎㅎ']

results = finance_classifier(target_data)

for result in results:
    print(f"label: {result['label']}, with score: {round(result['score'], 4)}")

