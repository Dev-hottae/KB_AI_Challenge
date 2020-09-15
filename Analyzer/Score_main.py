import json
import os
import sys
import pandas as pd
sys.path.insert(0, os.path.abspath('../'))

from transformers import pipeline, AutoModelForSequenceClassification
from kbpack.tokenization_kbalbert import KbAlbertCharTokenizer

# config.json open

config_path = r"C:\Users\dlagh\PycharmProjects\KB_AI_Challenge\Analyzer\finance_data\finance_config.json"

with open(config_path, "r") as jsonFile:
    data = json.load(jsonFile)

kb_albert_model_path = data['model_name_or_path']
model_output_path = data['output_dir']
model = AutoModelForSequenceClassification.from_pretrained(model_output_path)
tokenizer = KbAlbertCharTokenizer.from_pretrained(kb_albert_model_path)

classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer, framework='pt')

# reviews = ['이 영화 최악이었어!',
#            '볼거리가 많은 내 인생 영화 ㅎㅎ']

eval_data_path = r"C:\Users\dlagh\PycharmProjects\KB_AI_Challenge\Analyzer\finance_data\ratings_test.txt"
data = pd.read_csv(eval_data_path, encoding='utf-8', sep='\t')
reviews = data['content'].tolist()[:100]

results = classifier(reviews)
for idx, result in enumerate(results):
    print("="*20)
    print(reviews[idx])
    print(f"label: {result['label']}, with score: {round(result['score'], 4)}")
    print("=" * 20)