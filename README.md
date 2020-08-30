# KB_AI_Challenge

## 1. News Crawling

```python
scrapy crawl navernews <\filename.json> -a query='<\query>' -a start_date='<\start_date>' -a end_date='<\end_date>' -a time_break=<\time(option)>
```

## 2. News focus Crawling

```python
scrapy crawl naver_news_focus <\filename.json> -a start_date='<\start_date>' -a end_date='<\end_date(default:today)>' -a time_break=<\time(option)>
```
