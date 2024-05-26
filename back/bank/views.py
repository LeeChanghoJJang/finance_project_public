from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import requests
from django.conf import settings
from rest_framework.views import APIView
from .models import Deposit,DepositOption
from .serializers import DepositOptionsSerializer,DepositSerializer,DepositListSerializer
from stock.models import Stock
from stock.serializers import StockSerializer
from django.db.models import Subquery, OuterRef,FloatField
import matplotlib
import matplotlib.pyplot as plt 
import io
import base64
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
import seaborn as sns
import re
import random
# Matplotlib의 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def generate_chart_and_image(data, title, ylabel, image_variable):
    palettes = [
    'Blues', 'BuGn', 'BuPu', 'GnBu', 'PuBu', 'PuBuGn', 'PuRd', 'Purples', 

    ]   
    fig = plt.figure(figsize=(10, 5))
    fig.set_facecolor('white')
    selected_palette = random.choice(palettes)
    colors = sns.color_palette(selected_palette ,len(data))
    plt.bar(data.keys(), data.values(),color=colors)
    sns.lineplot(x=data.keys(), y=list(data.values()), palette=colors,linewidth=2)
    # plt.plot(data.keys(), list(data.values()),color='b',linestyle='-',marker='o',linewidth=2)
    # plt.title(title, fontsize=25,fontweight='heavy')
    plt.ylabel(ylabel,fontsize=15,fontweight='heavy')
    plt.xticks(rotation=25, ha='right',fontsize=11,fontweight='heavy')
    plt.tight_layout()
    # 현재 축 객체 가져오기
    ax = plt.gca()
    # 각 축의 테두리 두께 설정
    for spine in ax.spines.values():
        spine.set_linewidth(0)    
    # 이미지로 저장 후 base64로 인코딩하여 저장
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()
    image_variable = f'data:image/png;base64, {img_base64}'
    plt.close()
    return image_variable

def text_to_number(text):
    parts = text.split()
    total = 0
    unit_multipliers = {'경': 1e16, '조': 1e12, '억': 1e8, '만': 1e4}

    for part in parts:
        part = part.replace(',', '')
        match = re.match(r'(\d+)([경조억만]?)', part)
        if match:
            number, unit = match.groups()
            number = float(number)
            multiplier = unit_multipliers.get(unit, 1)
            total += number * multiplier

    return total
# 메인페이지에 있어야 할 모든 데이터를 반환한다.
@api_view(['GET'])
def main(request):
    matplotlib.use('Agg')
    url = f'http://ecos.bok.or.kr/api/KeyStatisticList/{settings.CENTER_BANK_API_KEY}/' + \
    f'json/kr/1/100/'
    product = requests.get(url).json()['KeyStatisticList']['row']
    combined_data = {'interest_rate':[],'exchange_rate':[],'market_index':[],'important_index':[]
                     ,'foreigner':[],'total_trade':[],'market_value':[],'dividend_ratio':[]}
    # 기준금리 / 콜금리 / 코리보금리 / CD금리 / 예금은행 수신금리 / 예금은행 대출금리
    combined_data['interest_rate'].append({
        'basemoneyrate':product[0]["DATA_VALUE"],
        'call_rate':product[1]["DATA_VALUE"],
        'koribor':product[2]["DATA_VALUE"],
        'cdrate':product[3]["DATA_VALUE"],
        'receipt_rate':product[8]["DATA_VALUE"],
        'credit_rate':product[9]["DATA_VALUE"],
    })
    # 원달러 환율 / 원엔환율 / 원유로환율 / 원위안화환율 / 외환보유액
    combined_data['exchange_rate'].append({
        'dollar':product[18]["DATA_VALUE"],
        'yen':product[19]["DATA_VALUE"],
        'euro':product[20]["DATA_VALUE"],
        'cny':product[21]["DATA_VALUE"],
        'foreign_exchange':product[86]["DATA_VALUE"],
    })
    # 코스피 / 코스닥 / 경제성장률 / GDP
    combined_data['market_index'].append({
        'kospi':product[22]["DATA_VALUE"],
        'kosdaq':product[23]["DATA_VALUE"],
        'growth':product[28]["DATA_VALUE"],
        'gdp':product[33]["DATA_VALUE"],
    })
    # 경제 심리지수 / 지니계수(불평등도) / 5분위 배율(불평등도) / 실업률 / 고용률
    combined_data['important_index'].append({
        'psychological':product[59]["DATA_VALUE"],
        'gini':product[65]["DATA_VALUE"],
        'five':product[66]["DATA_VALUE"],
        'unemploy':product[67]["DATA_VALUE"],
        'employ':product[68]["DATA_VALUE"],
    })
    
    foreigner = Stock.objects.order_by('-foreigner_ratio')[:10] # 외국인 보유율을 기준
    total_trade = Stock.objects.order_by('-total_trade')[:10] # 전체 거래량 기준
    market_value = Stock.objects.all()  # 모든 주식을 가져와서 후처리할 것임
    dividend_ratio = Stock.objects.order_by('-dividend_ratio')[:10] # 배당수익률 기준

    foreigner_serializer = StockSerializer(foreigner, many=True)
    total_trade_serializer = StockSerializer(total_trade, many=True)
    market_value_serializer = StockSerializer(market_value, many=True)
    dividend_ratio_serializer = StockSerializer(dividend_ratio, many=True)
    
    combined_data['foreigner'] = foreigner_serializer.data
    combined_data['total_trade'] = total_trade_serializer.data
    combined_data['market_value'] = sorted(
        market_value_serializer.data,
        key=lambda x: text_to_number(x['market_value']),
        reverse=True
    )[:10]
    combined_data['dividend_ratio'] = dividend_ratio_serializer.data
    
    # foreigner 차트 및 이미지 생성
    foreigner_chart_data = {item['name']: item['foreigner_ratio'] for item in combined_data['foreigner']}
    foreigner_image = generate_chart_and_image(foreigner_chart_data, 'Top 10 Stocks by Foreigner Ratio', 'Foreigner Ratio', 'image1')

    # total_trade 차트 및 이미지 생성
    total_trade_chart_data = {item['name']: item['total_trade'] for item in combined_data['total_trade']}
    total_trade_image = generate_chart_and_image(total_trade_chart_data, 'Top 10 Stocks by Total Trade', 'Total Trade', 'image2')

    # market_value 차트 및 이미지 생성
    market_value_chart_data = {item['name']: text_to_number(item['market_value']) for item in combined_data['market_value']}
    market_value_image = generate_chart_and_image(market_value_chart_data, 'Top 10 Stocks by Market Value', 'Market Value', 'image3')

    # dividend_ratio 차트 및 이미지 생성
    dividend_ratio_chart_data = {item['name']: item['dividend_ratio'] for item in combined_data['dividend_ratio']}
    dividend_ratio_image = generate_chart_and_image(dividend_ratio_chart_data, 'Top 10 Stocks by Dividend Ratio', 'Dividend Ratio', 'image4')

    # 이미지를 combined_data에 추가
    combined_data['image1'] = foreigner_image
    combined_data['image2'] = total_trade_image
    combined_data['image3'] = market_value_image
    combined_data['image4'] = dividend_ratio_image
    return JsonResponse(combined_data)

# 전체 예적금을 검색한다.
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def deposit_search(request):
    subquery = DepositOption.objects.filter(deposit=OuterRef('pk')).order_by('intr_rate').values('intr_rate')[:1]
    deposits = Deposit.objects.annotate(min_intr_rate=Subquery(subquery)).order_by('-min_intr_rate')
    serializer = DepositListSerializer(deposits, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 은행과 이자율 선택에 따라 검색한다.
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def deposit_search_by_params(request,bank_name,intr_rate_type):
    # 1. bank_name : 은행명
    # 2. intr_rate_type : 기본금리 / 최고금리 / 기본금리 3% 이상 / 최고금리 3%이상  
    # 필터링된 Deposit 쿼리셋
    deposits = Deposit.objects.filter(bank=bank_name)
    
    if intr_rate_type == '1':
        # intr_rate를 기준으로 정렬
        subquery = DepositOption.objects.filter(deposit=OuterRef('pk')).order_by('intr_rate').values('intr_rate')[:1]
        deposits = deposits.annotate(min_intr_rate=Subquery(subquery)).order_by('-min_intr_rate')
    elif intr_rate_type == '2':
        # intr_rate2를 기준으로 정렬
        subquery = DepositOption.objects.filter(deposit=OuterRef('pk')).order_by('intr_rate2').values('intr_rate2')[:1]
        deposits = deposits.annotate(min_intr_rate2=Subquery(subquery)).order_by('-min_intr_rate2')
    elif intr_rate_type == '3':
        # 기본금리가 3% 이상인 경우를 필터링하고 정렬
        subquery = DepositOption.objects.filter(deposit=OuterRef('pk')).order_by('intr_rate').values('intr_rate')[:1]
        deposits = deposits.annotate(min_intr_rate=Subquery(subquery, output_field=FloatField())).filter(min_intr_rate__gte=3).order_by('-min_intr_rate')
    elif intr_rate_type == '4':
        # 최고금리가 3% 이상인 경우를 필터링하고 정렬
        subquery = DepositOption.objects.filter(deposit=OuterRef('pk')).order_by('intr_rate2').values('intr_rate2')[:1]
        deposits = deposits.annotate(min_intr_rate2=Subquery(subquery, output_field=FloatField())).filter(min_intr_rate2__gte=3).order_by('-min_intr_rate2')
    
    serializer = DepositListSerializer(deposits, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# API를 호출하여 모든 예적금을 저장한다.
def save(request):
    url =  f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    # url =  f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
    # API 호출을 위한 파라미터 설정
    top_fin_grp_nos = ['020000', '030300']
    params = {
        'auth': settings.FSS_API_KEY,
        'pageNo': 1,
    }

    # API 호출 및 응답 처리
    for top_fin_grp_no in top_fin_grp_nos:
        params['topFinGrpNo'] = top_fin_grp_no
        response = requests.get(url, params=params)
        data = response.json()

        # # 데이터 파싱 및 모델에 저장
        # num = 0 
        # for item in data['result']['baseList']:
        #     num+=1
        #     # Deposit 모델 저장
        #     deposit ={
        #         'product_code': item['fin_prdt_cd'],
        #         'bank_code':item['fin_co_no'],
        #         'bank':item['kor_co_nm'],
        #         'etc_note':item['etc_note'],
        #         'product':item['fin_prdt_nm'],
        #         'max_limit':item['max_limit'],
        #         'start':item['dcls_strt_day'],
        #         'mtrt_int':item['mtrt_int'],
        #         'spcl_cnd':item['spcl_cnd'],
        #         'join_member':item['join_member'],
        #     }
        #     serializer_base = DepositSerializer(data=deposit)

        #     if serializer_base.is_valid(raise_exception=True):
        #         serializer_base.save()

        for item in data['result']['optionList']:
            deposit_option = {
                'period':int(item['save_trm']),
                'intr_type':item['intr_rate_type_nm'],
                'intr_rate': float(item['intr_rate']) if item.get('intr_rate') is not None else 0.0,
                'intr_rate2': float(item['intr_rate2']) if item.get('intr_rate2') is not None else 0.0,
                'deposit': Deposit.objects.filter(product_code=item['fin_prdt_cd']).first().pk,
                'rsrv_type_nm':item.get('rsrv_type_nm',None)
            }
            serializer_base = DepositOptionsSerializer(data=deposit_option)

            if serializer_base.is_valid(raise_exception=True):
                serializer_base.save()     
    return JsonResponse({'message':'ok'},safe=True)

# 데이터 싹다 지우는 함수
def clear(request):
    # Deposit.objects.all().delete()
    DepositOption.objects.all().delete()

class UpdateDepositUserView(APIView):
    def post(self, request, deposit_id):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

        print(deposit_id)
        deposit = get_object_or_404(Deposit, id=deposit_id)

        if request.user in deposit.users.all():
            deposit.users.remove(request.user)
            action = 'removed'
        else:
            deposit.users.add(request.user)
            action = 'added'
        deposit.save()
        
        serializer = DepositSerializer(deposit)
        response_data = {
            'deposit': serializer.data,
            'action': action
        }
        
        return Response(response_data, status=status.HTTP_200_OK)