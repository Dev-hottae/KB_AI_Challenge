import pandas as pd
import numpy as np
import itertools
import nltk
import copy
import datetime
import os
import requests
from bs4 import BeautifulSoup

class NBC():
    def add_data(self, datas):
        word_column = datas.columns[1]
        target_column = datas.columns[2]
        target_ls = list(set(datas[target_column]))
        # list가 아닐 경우 실행
        # datas[word_column] = list(map(lambda i : i.split(','), datas[word_column]))

        total_ngram = list(itertools.chain(*list(datas[word_column]))) 
        unique_ngram = list(set(total_ngram))
        result_df = pd.DataFrame(unique_ngram, columns = [word_column]).set_index(word_column)
        for target in target_ls:
            this_ngram = list(itertools.chain(*list(datas[datas[target_column] == target][word_column])))
            fdist = nltk.FreqDist(this_ngram)
            temp_df = pd.DataFrame(list(zip(fdist.keys(), fdist.values())), columns= [word_column, 'count']).set_index(word_column)
            result_df[target] = temp_df['count']
        
        result_df.fillna(0, inplace=True)
        result_df['score'] = 0
        self.df = copy.deepcopy(result_df)
        return self.df

    # 샘플된 데이터에 대한 카운트 매트릭스 생성
    def count_vec(self, datas):
        word_column = datas.columns[0]
        target_column = datas.columns[1]
        target_ls = list(set(datas[target_column]))

        total_ngram = list(itertools.chain(*list(datas[word_column]))) 
        unique_ngram = list(set(total_ngram))
        result_df = pd.DataFrame(unique_ngram, columns = [word_column]).set_index(word_column)
        
        for target in target_ls:
            this_ngram = list(itertools.chain(*list(datas[datas[target_column] == target][word_column])))
            fdist = nltk.FreqDist(this_ngram)
            temp_df = pd.DataFrame(list(zip(fdist.keys(), fdist.values())), columns= [word_column, 'count']).set_index(word_column)
            result_df[target] = temp_df['count']

        result_df.fillna(0, inplace=True)
        return result_df
    
    # 극성점수 계산
    def polarity_score(self, datas):
        df = datas
        
        df['haw'] = df[1] / sum(df[1])
        df['dov'] = df[-1] / sum(df[-1])
        df['count'] = 1
        self.df['score'] += df['haw'] / df['dov']
        self.df['count'] += df['count']
        return self.df

    # 배깅하면서 나온 횟수만큼만 나눠줌 (30으로 나눠버리면 수치가 달라짐)
    # 30회 배깅
    def bagging(self, train_data, k):
        self.df['count'] = 0
        for i in range(k):
            self.polarity_score(self.count_vec(train_data.sample(frac=0.9)))

        self.df['score'] = self.df['score'] / self.df['count']
        return self.df[self.df['count'] != 0]

class Testing():
    # 파일 위치 지정 ※
    def load_datas(self, test_dir='testing'):
        # 학습 DATA 불러오기
        
        train_data = pd.read_json(test_dir+'/final_ngram_comma.json')
        train_data['date'] = list(map(lambda i : i.date(), train_data['date']))
        train_data.set_index('date', inplace=True)
        # 학습 기간 설정
        train_data = train_data.iloc[(train_data.index >= datetime.date(2005,5,1)) & 
                                    (train_data.index <= datetime.date(2017,12,31))]
        # 클래스 사용 위해 데이터 분리
        train_data['ngram'] = list(map(lambda i : i.split(','), train_data['ngram']))

        # 기준 금리 데이터, 경로 설정
        sr_df = pd.read_json(test_dir+'/standard_rate.json').set_index('date')

        # Load Test Data, 날짜 하나로 NGRAM 합침
        test_data = pd.read_json(test_dir+'/test_ngram_datas.json')
        test_data['ngram'] = list(map(lambda i : i.split(','), test_data['ngram']))
        test_data['date'] = list(map(lambda i : i.date(), test_data['date']))
        test_data = test_data[test_data['date'] <= datetime.date(2017,12,31)]

        # Load Rate Data
        call_data = pd.read_json(test_dir + '/rate_data/labeled_cd_rate.json').set_index('date')

        return train_data, call_data, test_data, sr_df

