# KB_AI_Challenge
-----------------------------
2020 KB AI 챌린지

## 대회 개요
-------------------------------
KB-ALBERT를 활용한 금융 자연어 서비스 아이디어 제공
> 대회관련 홈페이지 : http://www.kbdatory.com/

## 서비스 주제
------------------------------------
1. 네이버 키워드를 통한 향후 경제시장지표 예측(ex> 금리, 달러, 금 등)
2. 국내 경기 상황을 잘 나타낼 수 있는 경기지수 생성

## 프로세스
--------------------------
데이터 수집
> 1. 뉴스사 및 지정 키워드를 기반한 뉴스 텍스트 데이터 수집
> 2. 경제 관련 지표 데이터 수집
> 3. 예측에 활용할 리포트 데이터 수집

데이터 전처리
>

데이터 분석
>

활용(예측)
>

-------------
## 패키지 활용
### 1. News Crawling

```python
scrapy crawl navernews <\filename.json> -a query='<\query>' -a start_date='<\start_date>' -a end_date='<\end_date>' -a time_break=<\time(option)>
```

### 2. News focus Crawling

```python
scrapy crawl naver_news_focus <\filename.json> -a start_date='<\start_date>' -a end_date='<\end_date(default:today)>' -a time_break=<\time(option)>
```
