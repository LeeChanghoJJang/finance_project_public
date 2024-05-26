from .models import Stock
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import matplotlib.pyplot as plt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests
import random
from django.conf import settings
import json
import urllib.request
import pandas as pd
from .serializers import StockSerializer,DailyStockSerializer,RelatedCorporationSerializer,ResearchSerializer,FinanceSerializer,StockFirstSerializer, ArticleListSerializer, CommentListSerializer, ArticleSerializer, CommentSerializer
from .models import Stock,RelatedCorporation,Research,Finance,DailyStock,Article,Comment
import OpenDartReader
from datetime import datetime, timedelta
import FinanceDataReader as fdr
from bank.models import DepositOption
from django.db.models import F, ExpressionWrapper, IntegerField,FloatField
from django.db.models.functions import Cast
from bank.serializers import DepositOptionsAllSerializer,DepositOptionCompound1Serializer,DepositOptionCompound2Serializer
import base64
import io
from matplotlib.ticker import MaxNLocator
import matplotlib
import seaborn as sns
from review.models import Review
import random

# 주식 기본페이지 함수(삼성전자를 입력하면 주식검색이 된다)
@api_view(['GET'])
def stock_search(request,stock_name):
    if request.method == 'GET':
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] = False
        stocks = Stock.objects.filter(name=stock_name).first()
        relation_corporation = RelatedCorporation.objects.filter(stock=stocks.pk)
        researches = Research.objects.filter(stock=stocks.pk)
        finances = Finance.objects.filter(stock=stocks.pk)
        combined_data = {}

        url = f'https://openapi.naver.com/v1/search/news.json'
        params = {
            'query':stock_name,
            'display':10,
            'start':100,
            'sort':'date',
        }
        headers = {
            'X-Naver-Client-Id': 'IlflCaQUqRlpgc_OG_jU',
            'X-Naver-Client-Secret': 'Oq4sU1LEOp'
        }

        response = requests.get(url,headers=headers,params=params).json().get('items')
        
        combined_data = {'naversearch':[],'stock_info':[],'finances':[],'relation_corporation':[],'researches':[],'article_titles':[],'company_list':[]}
        # 기업소식 : 네이버 검색 데이터 
        for item in response:
            combined_data['naversearch'].append({
                'title': item.get('title', ''),
                'link': item.get('link', ''),
                'description': item.get('description', ''), 
            })

        # 주식정보
        combined_data['stock_info'] = {
            'name': stocks.name,
            'stock_code': stocks.stock_code,
            'dividend_ratio': stocks.dividend_ratio,
            'foreigner_ratio': stocks.foreigner_ratio,
            'foreigner_buy':stocks.foreigner_buy,
            'price':stocks.price,
            'individual_buy' :stocks.individual_buy,
            'organ_buy':stocks.organ_buy,
            'total_trade' :stocks.total_trade,
            'dividend':stocks.dividend,
            'pbr':stocks.pbr,
            'per':stocks.per,
            'highprice_52':stocks.highprice_52,
            'lowprice_52':stocks.lowprice_52,
            'market_value' :stocks.market_value,
        }
        # 연관 기업정보
        for item in relation_corporation:
            combined_data['relation_corporation'].append({
                'name': item.name,
                'url': item.url,
            })
        # 리서치 정보 
        if researches:
            for item in researches:
                combined_data['researches'].append({
                    'name': item.name,
                    'title': item.title,
                    'date': item.date, 
                    'reporter': item.reporter,
                    'url':item.url,
                })
        # 재무정보
        if finances:
            for item in finances:
                combined_data['finances'].append({
                    'revenue': item.revenue,
                    'operating_pr': item.operating_pr,
                    'profits': item.profits,
                    'fluid_asset': item.fluid_asset,
                    'fluid_liabilites': item.fluid_liabilites,
                    'total_equity': item.total_equity,
                    'total_liabilites': item.total_liabilites,
                })

        # 해당 주식에 대한 게시글 제목 추가
        reviews = Review.objects.filter(stock=stocks.pk)
        for review in reviews:
            combined_data['article_titles'].append({review.pk: review.title})

        # 주식 기업 리스트 추가
        all_stocks = Stock.objects.all()
        for stock in all_stocks:
            combined_data['company_list'].append(stock.name)

        return Response(combined_data,status=status.HTTP_200_OK)
    
# 주식 상세페이지 함수(삼성전자를 입력하면 주식검색이 된다)
@api_view(['GET'])
def stock_search_detail(request,stock_name):
    matplotlib.use('Agg')
    plt.rcParams['font.family'] ='Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] =False
    if request.method == 'GET':
        stocks = Stock.objects.get(name=stock_name)
        finances = Finance.objects.filter(stock=stocks.pk)
        daily_stock = DailyStock.objects.filter(stock=stocks.pk)
        combined_data = {'finances':[],'stock_info':[]}
        # 주식정보
        combined_data['stock_info'] = {
            'name': stocks.name,
            'stock_code': stocks.stock_code,
            'dividend_ratio': stocks.dividend_ratio,
            'foreigner_ratio': stocks.foreigner_ratio,
            'foreigner_buy':stocks.foreigner_buy,
            'price':stocks.price,
            'individual_buy' :stocks.individual_buy,
            'organ_buy':stocks.organ_buy,
            'total_trade' :stocks.total_trade,
            'dividend':stocks.dividend,
            'pbr':stocks.pbr,
            'per':stocks.per,
            'highprice_52':stocks.highprice_52,
            'lowprice_52':stocks.lowprice_52,
            'market_value' :stocks.market_value,
        }
        
        # 재무정보
        if finances:
            for item in finances:
                combined_data['finances'].append({
                    'revenue': item.revenue,
                    'operating_pr': item.operating_pr,
                    'fluid_asset': item.fluid_asset,
                    'fluid_liabilites': item.fluid_liabilites,
                    'total_equity': item.total_equity,
                    'total_liabilites': item.total_liabilites,
                })
                
        if daily_stock:
        
            # 주가 추이 그래프 생성
            dates = [item.date[5:10] for item in daily_stock]
            prices = [item.price for item in daily_stock]

            palettes = [
            'Blues', 'BuGn', 'BuPu', 'GnBu', 'Greens', 'Oranges',
            'OrRd', 'PuBu', 'PuBuGn', 'PuRd', 'Purples', 
            'RdPu', 'Reds' 

            ]   
            # 그래프 생성
            fig = plt.figure(figsize=(10, 5))
            fig.set_facecolor('white')
            selected_palette = random.choice(palettes)
            colors = sns.color_palette(selected_palette ,len(prices))
            # sns.set(style='whitegrid')
            # sns.lineplot(x=dates, y=prices, marker='o')
            sns.lineplot(x=dates, y=prices, palette=colors,linewidth=2)
            plt.title(f'{stock_name} Stock Price Over Time',fontsize=25,fontweight='heavy')
            plt.xlabel('Date',fontsize=15,fontweight='heavy')
            plt.ylabel('Price',fontsize=15,fontweight='heavy')
            plt.xticks(rotation=45, ha='right',fontsize=13,fontweight='heavy')
            plt.tight_layout()
            plt.grid(True)
            # 각 축의 테두리 두께 설정
            ax = plt.gca()
            ax.xaxis.set_major_locator(MaxNLocator(integer=True, prune='both'))
            for spine in ax.spines.values():
                spine.set_linewidth(2)  
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.gca().yaxis.grid(alpha=0.1)

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
            buffer.close()
            combined_data['image'] = f'data:image/png;base64, {img_base64}'
            plt.close()

            # 클라이언트에게 제공할 이미지 데이터를 JSON에 포함
            # return render(request,'./stock.html',combined_data)

        return Response(combined_data,status=status.HTTP_200_OK)

# 주식정보 저장 함수(API 호출하면 됨) => 기능별 각각 저장해야 함
# @login_required
def save(request):
    dart = OpenDartReader(settings.OPEN_DART_API_KEY)
    allstock = pd.read_csv('allstocks.csv',encoding='cp949')
    num = 0
    for (idx,item_code) in enumerate(allstock['단축코드'],1):
        if idx > 2807:
            break

        url = f"https://m.stock.naver.com/api/stock/{item_code:>06s}/integration"
        raw_data = urllib.request.urlopen(url).read()
        json_data = json.loads(raw_data) #추후, 데이터 가공을 위해 json 형식으로 변경 합니다.
        total_info = json_data['totalInfos'] 
        dealtrend = json_data['dealTrendInfos']
        
        # 주식정보
        try:
            stock = {
                'name': json_data['stockName'],
                'stock_code': f'{item_code:>06s}',
                'dividend_ratio': 0 if not total_info[16].get('value') or not total_info[16].get('value')[:-1].replace('.', '').isdigit() else float(total_info[16]['value'][:-1]),
                'foreigner_ratio': round(float(total_info[7].get('value', 0).replace('%', '')) / 100,2),
                'foreigner_buy': int(dealtrend[0]['foreignerPureBuyQuant'].replace(',', '')) if dealtrend[0]['foreignerPureBuyQuant'].replace(',', '').isdigit() else 0,
                'price': int(total_info[0]['value'].replace(',', '')) if total_info[0]['value'].replace(',', '').isdigit() else 0,
                'individual_buy': int(dealtrend[0]["individualPureBuyQuant"].replace(',', '')) if dealtrend[0]["individualPureBuyQuant"].replace(',', '').isdigit() else 0,
                'organ_buy': int(dealtrend[0]["organPureBuyQuant"].replace(',', '')) if dealtrend[0]["organPureBuyQuant"].replace(',', '').isdigit() else 0,
                'total_trade': int(total_info[4]['value'].replace(',', '')) if total_info[4]['value'].replace(',', '').isdigit() else 0,
                'dividend': 0 if not total_info[17].get('value') or not total_info[17].get('value')[:-1].replace(',', '').isdigit() else int(total_info[17]['value'][:-1].replace(',', '')),
                'per': round(float(total_info[10]['value'].replace(',', '').replace('배', '')),2) if total_info[10]['value'] and total_info[10]['value'] != 'N/A' and total_info[10]['value'].replace(',', '').replace('배', '').replace('.', '').isdigit() else 0,
                'pbr': round(float(total_info[14]['value'].replace(',', '').replace('배', '')),2) if total_info[14]['value'] and total_info[14]['value'] != 'N/A' and total_info[14]['value'].replace(',', '').replace('배', '').replace('.', '').isdigit() else 0,
                'highprice_52': int(total_info[8]['value'].replace(',', '')) if total_info[8]['value'].replace(',', '').isdigit() else 0,
                'lowprice_52': int(total_info[9]['value'].replace(',', '')) if total_info[9]['value'].replace(',', '').isdigit() else 0,
                'market_value': total_info[6]['value'],
            }
            serializer_base = StockSerializer(data=stock)
            if serializer_base.is_valid(raise_exception=True):
                serializer_base.save()
            num+=1
            # 현재 날짜 구하기
            today = datetime.now() 
            yesterday = today - timedelta(days=1) 

            # 3달 전의 날짜 계산
            three_months_ago = today - timedelta(days=90)

            prices = fdr.DataReader(f'{item_code:>06s}', three_months_ago.strftime("%Y-%m-%d"), yesterday.strftime("%Y-%m-%d")).Close
            # 주어진 데이터를 순회하면서 serializer를 사용하여 DB에 저장
            for date, price in prices.items():
                # 문자열 형태의 날짜를 datetime 객체로 변환
                # 해당 날짜와 가격을 serializer에 전달하여 저장
                serializer = DailyStockSerializer(data={'date': str(date), 'price': round(price), 'stock': num})
                if serializer.is_valid():
                    serializer.save() 
            # 리서치
            if json_data['researches']:
                researches = json_data['researches']
                for res in researches:
                    try:
                        if not Research.objects.filter(title=res['tit'], name=res['nm']).exists():
                            research ={
                                    'name':res['nm'],
                                    'title':res['tit'],
                                    'date':res['wdt'],
                                    'reporter':res['bnm'],
                                    'stock':num,
                                    'url':f'https://m.stock.naver.com/domestic/stock/{res["cd"]}/research/{res["id"]}'
                                    }
                            serializer_base = ResearchSerializer(data=research)

                            if serializer_base.is_valid(raise_exception=True):
                                serializer_base.save()

                    except Exception as e:
                        pass

            # 연관기업
            if json_data['industryCompareInfo']:
                industry = json_data['industryCompareInfo']
                for i in industry:
                    try:
                        related_cor ={
                                'name':i['stockName'],
                                'stock':num,
                                'url':f'http://127.0.0.1:8000/stock/{i["stockName"]}/search/',
                                }
                        serializer_base = RelatedCorporationSerializer(data=related_cor)

                        if serializer_base.is_valid(raise_exception=True):
                            serializer_base.save()
                    except Exception as e:
                        pass
            # 재무정보
            if '우' != json_data['stockName'][-1] and all(item not in json_data['stockName'] for item in ['우(전환)','우B','1우','2우']):    
                finances = dart.finstate(f'{item_code:>06s}',2023,reprt_code='11011')
                
                if finances is not None and not finances.empty:
                    finances = finances['thstrm_amount']
                    try:
                        finance ={
                                'revenue':int(finances[9].replace(',','')) if finances[9] else 0,
                                'operating_pr':int(finances[10].replace(',','')) if finances[10] else 0,
                                'profits':int(finances[12].replace(',','')) if finances[12] else 0,
                                'fluid_asset':int(finances[0].replace(',','')) if finances[0] else 0,
                                'fluid_liabilites':int(finances[3].replace(',','')) if finances[3] else 0,
                                'total_equity':int(finances[8].replace(',','')) if finances[8] else 0,
                                'total_liabilites':int(finances[5].replace(',','')) if finances[5] else 0,
                                'stock':num
                                }
                        serializer_base = FinanceSerializer(data=finance)

                        if serializer_base.is_valid(raise_exception=True):
                            serializer_base.save()
                    except Exception as e:
                        pass
        except Exception as e:
            pass

    return JsonResponse({'message':'ok'})

def clear(request):
    Research.objects.all().delete()
    # RelatedCorporation.objects.all().delete()
    # Finance.objects.all().delete()

def get_three_months_ago_price(stock):
    for days_ago in range(90, 85, -1):
        date_to_check = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d 00:00:00')
        try:
            oldest_stock = stock.daily_stock.filter(date=date_to_check).order_by('date').first()
            if oldest_stock:
                return oldest_stock.price
        except DailyStock.DoesNotExist:
            continue
    return None

@api_view(['GET'])
def recommend(request,standard):
    stocks = Stock.objects.all()
    
    stock_diffs = []
    for stock in stocks:
        three_months_ago_price = get_three_months_ago_price(stock)
        if three_months_ago_price is not None:
            if standard == 1:
                # 매매차익 기준 100개 기업 선정
                diff = abs((stock.price - three_months_ago_price) / three_months_ago_price * 100)
            elif standard == 2:
                # 매매차익 + 배당수익 기준 100개 기업 선정
                try :
                    diff = abs((float(stock.price) - float(three_months_ago_price)) / float(three_months_ago_price) * 100 + float(stock.dividend_ratio))
                except ZeroDivisionError :
                    continue
            elif standard == 3:
                # 변동성 기준 100개 기업 선정
                try : 
                    diff = abs((float(stock.highprice_52) - float(stock.lowprice_52)) / float(stock.lowprice_52) * 100 + float(stock.dividend_ratio))
                except ZeroDivisionError :
                    continue 
            stock_diffs.append((stock, diff))
    
    # 1단계: 수익률 기준 순서대로 100개 기업 선정 
    sorted_stocks_with_diff = sorted(stock_diffs, key=lambda x: x[1], reverse=True)[:100]
    recommended_stock_ids = [stock[0].id for stock in sorted_stocks_with_diff]
    recommended_stocks = Stock.objects.filter(id__in=recommended_stock_ids)
    
    # 2단계: 재무건전성 조건 충족
    filtered_finances = Finance.objects.filter(
        total_liabilites__lte=F('total_equity') * 2,
        fluid_asset__gte=F('fluid_liabilites') * 2,
        operating_pr__gte=0
    )
    filtered_stock_ids = filtered_finances.values_list('stock_id', flat=True)
    
    # 재무건전성을 충족하는 stock id를 기준으로 필터링 1개만 선정
    final_recommended_stocks = recommended_stocks.filter(id__in=filtered_stock_ids)
    final_recommended_stocks_serialized = StockFirstSerializer(final_recommended_stocks,many=True)
    # 최종 추천된 주식을 무작위로 선택
    final_recommended_stocks = random.choice(final_recommended_stocks)
    
    # 선택된 주식에 대한 Serializer 생성
    final_recommended_stocks_serialized = StockFirstSerializer(final_recommended_stocks, context={'standard': standard})
    
    # 1단계 : 단리면서, 기간이 12개월 이상과 12개월 미만 예금 
    deposit_options1 = DepositOption.objects.filter(rsrv_type_nm__isnull=True,
        period__gte=12, intr_type='단리').order_by('-intr_rate')
    deposit_options2 = DepositOption.objects.filter(rsrv_type_nm__isnull=True,
        period__lt=12, intr_type='단리').order_by('-intr_rate')

    # 2단계 : 연 복리 예금
    deposit_options3 = DepositOption.objects.filter(rsrv_type_nm__isnull=True,
        period__gte=12, intr_type='복리').annotate(
        effective_rate3=ExpressionWrapper(
            (1 + F('intr_rate') / 100 / 12) ** (Cast(F('period') / 12, output_field=IntegerField())) - 1,
            output_field=FloatField()
        )).order_by('-effective_rate3')
    

    deposit_options4 = DepositOption.objects.filter(rsrv_type_nm__isnull=True,
        period__lt=12, intr_type='복리').annotate(
        effective_rate4=ExpressionWrapper(
            (1 + F('intr_rate') / 100 / 12) ** (Cast(F('period') / 12, output_field=IntegerField())) - 1,
            output_field=FloatField()
        )).order_by('-effective_rate4')
    
    # 3단계 : 월 복리면서, 기간이 12개월 이상과 12개월 미만 적금
    deposit_options5 = DepositOption.objects.filter(rsrv_type_nm__isnull=False,
        period__gte=12, intr_type='복리').annotate(
        effective_rate5=ExpressionWrapper(
            F('intr_rate') / 100 * (F('period')+1) / 24,
            output_field=FloatField()
        )
        ).order_by('-effective_rate5')
    
    deposit_options6 = DepositOption.objects.filter(rsrv_type_nm__isnull=False,
        period__lt=12, intr_type='복리').annotate(
        effective_rate6=ExpressionWrapper(
            F('intr_rate') / 100 * (F('period')+1) / 24,
            output_field=FloatField()
        )).order_by('-effective_rate6')

    # 4단계 : 단복리 / 기간 / 예적금 및 기본금리에 따라 분리
    deposit_options_1 = DepositOptionsAllSerializer(deposit_options1.first())
    deposit_options_2 = DepositOptionsAllSerializer(deposit_options2.first())
    deposit_options_3 = DepositOptionCompound1Serializer(deposit_options3.first())
    deposit_options_4 = DepositOptionCompound1Serializer(deposit_options4.first())
    deposit_options_5 = DepositOptionCompound2Serializer(deposit_options5.first())
    deposit_options_6 = DepositOptionCompound2Serializer(deposit_options6.first())
    
    combined_data = {
        'recommend_stock' : final_recommended_stocks_serialized.data,
        
        }

    # 최대 수익률 찾기 (예적금)
    max_value = max(deposit_options_1.data['intr_rate'], 
    deposit_options_2.data['intr_rate'],
    deposit_options_3.data['effective_rate'],
    deposit_options_4.data['effective_rate'],
    deposit_options_5.data['effective_rate'],
    deposit_options_6.data['effective_rate'])
    depositsoptions = [deposit_options_1,deposit_options_2,deposit_options_3,deposit_options_4,deposit_options_5,deposit_options_6]
    max_value = 0
    for i,j in enumerate(depositsoptions):
        if i<2:
            if max_value < j.data['intr_rate']:
                max_value = j.data['intr_rate']
                combined_data['max_deposit'] = j.data
        else:
            if max_value < j.data['effective_rate']:
                max_value = j.data['effective_rate']
                combined_data['max_deposit'] = j.data
    return Response(combined_data)

@api_view(['GET','POST',])
def article_list(request, stock_name):
    stock = Stock.objects.get(name=stock_name)
    # 조회
    if request.method == 'GET': 
        # 필터로 변경해야함
        articles = Article.objects.filter(stock=stock).order_by('-pk')
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    # 생성
    elif request.method == 'POST': 
        serializer = ArticleSerializer(data=request.data)      
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, stock=stock)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, stock_name, article_pk):
    stock = Stock.objects.get(name=stock_name)
    article = Article.objects.get(pk=article_pk)
    if request.method == "GET":
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, stock=stock)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == "DELETE":
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def comment_list(request, stock_name, article_pk):
    article = Article.objects.get(pk=article_pk)
    comments = Comment.objects.filter(article=article)
    
    if request.method == "GET" :
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == "POST" :
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def comment_delete(request, stock_name, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)