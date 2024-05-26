from django.db import models
from django.conf import settings

# Create your models here.

class Stock(models.Model):
    name = models.TextField() # 주식명
    stock_code = models.TextField() # 종목코드
    dividend_ratio = models.FloatField(blank=True,null=True) # 배당수익률
    foreigner_ratio = models.FloatField() # 외국인 소진율
    foreigner_buy = models.IntegerField() # 외국인 순매수
    price = models.IntegerField() # 전일 종가
    individual_buy = models.IntegerField() # 개인 순매수
    organ_buy = models.IntegerField() # 기관 순매수
    total_trade = models.IntegerField() # 거래량
    dividend = models.TextField(blank=True,null=True) # 배당금
    pbr = models.FloatField() # 기업 PBR
    per = models.FloatField() # 기업 PER 
    highprice_52 = models.IntegerField() # 52주 최고가
    lowprice_52 = models.IntegerField() # 52주 최저가
    market_value = models.TextField() # 시가총액

class UserStock(models.Model):
    amount = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

class DailyStock(models.Model):
    date =models.TextField() # 해당 주식의 일자
    price = models.IntegerField() # 주가(종가)
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE,related_name='daily_stock') # 주식과 연결된 외래키 

class Research(models.Model):
    name = models.TextField() # 주식명
    title = models.TextField() # 리서치 제목
    date = models.TextField() # 리서치 쓴 날짜
    reporter = models.TextField() # 리서치 쓴 증권사
    url = models.TextField() # 리서치 링크 연결할 url
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE,related_name='researches') # 주식과 연결된 외래키 

class RelatedCorporation(models.Model):
    name = models.TextField() # 관계기업명
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE,related_name='related_corporations') # 주식과 연결된 외래키 
    url = models.TextField(blank=True,null=True) # url

class Finance(models.Model):
    revenue = models.IntegerField()
    operating_pr = models.IntegerField()
    profits = models.IntegerField()
    fluid_asset = models.IntegerField()
    fluid_liabilites = models.IntegerField()
    total_equity = models.IntegerField()
    total_liabilites = models.IntegerField()
    stock = models.ForeignKey(Stock,on_delete =models.CASCADE,related_name='finances')

## 게시글
class Article(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

## 댓글
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)