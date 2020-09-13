from kbpack import FileSearch
import pandas as pd
fl = FileSearch.Search().data_search('/home/lab10/JJC/KB_AI_Challenge/Analyzer/result/final', '.txt')

final_df = pd.DataFrame()
for f in fl:
    final_df = pd.concat([final_df, pd.read_csv(f)])

vix_df = pd.read_csv('/home/lab10/JJC/KB_AI_Challenge/Analyzer/hottae_data/vix.csv')

final_df = final_df.groupby('date').mean()
vix_df.set_index('date', inplace=True)

vix_df['score'] = final_df['score']

print(vix_df[['vix','score']].corr())

vix_df.to_csv('final.csv')