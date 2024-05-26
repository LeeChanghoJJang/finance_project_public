from rest_framework import serializers
from .models import Stock, DailyStock,Research,RelatedCorporation,Finance,UserStock, Article, Comment
from datetime import datetime, timedelta

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class DailyStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyStock
        fields = '__all__'

class ResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Research
        fields = '__all__'

class RelatedCorporationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedCorporation
        fields = '__all__'

class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = '__all__'
        
class StockFirstSerializer(serializers.ModelSerializer):
    price_diff1 = serializers.SerializerMethodField()
    price_diff2 = serializers.SerializerMethodField()
    price_diff3 = serializers.SerializerMethodField()
    effective_rate = serializers.SerializerMethodField()

    def get_three_months_ago_price(self, obj):
        for days_ago in range(90, 85, -1):
            date_to_check = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d 00:00:00')
            print(f"Checking date: {date_to_check}")  # 디버깅 출력
            try:
                oldest_stock = obj.daily_stock.filter(date=date_to_check).order_by('date').first()
                if oldest_stock:
                    print(f"Found price {oldest_stock.price} for date {date_to_check}")  # 디버깅 출력
                    return oldest_stock.price
            except DailyStock.DoesNotExist:
                continue
        return None
    
    def get_price_diff1(self, obj):
        # 3개월 전 데이터를 가져옴
        three_months_ago_price = self.get_three_months_ago_price(obj)
        if three_months_ago_price is not None:
            return round((obj.price - three_months_ago_price) / three_months_ago_price * 100,3)
        return None

    def get_price_diff2(self, obj):
        # 3개월 전 데이터를 가져옴
        three_months_ago_price = self.get_three_months_ago_price(obj)
        if three_months_ago_price is not None:
            return round((obj.price - three_months_ago_price) / three_months_ago_price * 100 + obj.dividend_ratio,3)
        return None

    def get_price_diff3(self, obj):
        # 변동성 기준으로 price_diff 계산
        if obj.lowprice_52:
            return round((obj.highprice_52 - obj.lowprice_52) / obj.lowprice_52 * 100,3)
        return None
    
    def get_effective_rate(self, obj):
        # 3개월 전 데이터를 가져옴
        if self.context.get('standard') == 1:
            return self.get_price_diff1(obj)
        elif self.context.get('standard') == 2:
            return self.get_price_diff2(obj)
        elif self.context.get('standard') == 3:
            return self.get_price_diff3(obj)
        
    class Meta:
        model = Stock
        fields = '__all__'

class UserStockSerializer(serializers.ModelSerializer):
    stock = StockSerializer()
    class Meta:
        model = UserStock
        fields = ['amount', 'stock',]

class UserStockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStock
        fields = ['amount', 'stock', 'user']

class CommentListSerializer(serializers.ModelSerializer):
    class Meta :
        model = Comment
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)

class ArticleListSerializer(serializers.ModelSerializer):
    comment_set = CommentListSerializer(many=True, read_only=True)  # 댓글을 포함

    class Meta :
        model = Article
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at', 'comment_set']

class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentListSerializer(many=True, read_only=True)  # 댓글을 포함

    class Meta:
        model = Article
        fields = ('title','content','comment_set')
