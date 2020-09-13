from kbpack.kb_package import NBC
import pandas as pd
import copy
import numpy as np

nbc = NBC()

datas = pd.read_csv('/home/lab10/JJC/KB_AI_Challenge/Analyzer/hottae_data/vix7_data/finance_train.txt', sep='\t')
print('bagging 시작')
nbc.add_data(datas)
nbc.bagging(datas, 1)
print('bagging 끝')
hawkish = nbc.df[nbc.df['score'] >= 1.3].index
dovish = nbc.df[nbc.df['score'] <= 10/13].index

print(len(hawkish), len(dovish))

def tone_sent(x):
    a = 0
    b = 0
    for ngram in x:
        if ngram in hawkish:
            a += 1
        elif ngram in dovish:
            b += 1
    # if a+b < ngram_limit:
    #     return np.nan
    try:
        return (a-b) / (a+b)
    except:
        return np.nan

print('Score 계산')
test_data = pd.read_csv('/home/lab10/JJC/KB_AI_Challenge/Analyzer/hottae_data/vix7_data/finance_test.txt', sep='\t')
# Tone 계산 (문장 -> 문서)
# Tokne 칼럼 설정
test_data['tone'] = list(map(tone_sent, test_data['text']))

tone_data = copy.deepcopy(test_data.dropna())
# 0은 중립
tone_data['HD'] = list(map(lambda i : 'H' if i > 0 else 'D' if i < 0 else np.nan, tone_data['tone']))
tone_data.dropna(inplace=True)
tone_data['H'] = list(map(lambda i : 1 if i == 'H' else 0, tone_data['HD']))
tone_data['D'] = list(map(lambda i : 1 if i == 'D' else 0, tone_data['HD']))
final_tone = copy.deepcopy(tone_data.groupby('date').sum()[['H','D']])

# 남은 문장이 sl개를 넘는 BOK 문서만 계산 (이상치 제거)
# 10개 이하 자르면 160개 정도 나오는 것을 확인
# sl = 10
# final_tone = final_tone[final_tone['H'] + final_tone['D'] > sl]
final_tone['tone'] = (final_tone['H'] - final_tone['D']) / (final_tone['H'] + final_tone['D'])

final_tone.to_csv('final_result.csv')

print('학습 끝')
# 상관분석
# final_tone['rate'] = sr_df['rate']

# corr = final_tone['tone'].corr(final_tone['rate'], method = 'pearson')
# call_corr.append([dc, rl, len(final_tone), corr])
# print('Date Range:', dc, "Rate Limit:", rl, '\nTest 개수:', len(final_tone), 'Corr :', corr)

# Hawkish, Dovish 사전 추출
# if corr > 0.68 or corr < 0.3:
#     pd.DataFrame([hawkish, dovish]).to_json('testing/dictionary/hawkish_dovish_{}_{}.json'.format(dc, rl))
# print()