from rest_framework import serializers
from .models import Deposit,DepositOption

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        exclude = ('users',)  # users 필드 제외


class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'

class DepositOptionsAllSerializer(serializers.ModelSerializer):
    deposit = DepositSerializer()
    class Meta:
        model = DepositOption
        fields = '__all__'

class DepositOptionListSerializer(serializers.ModelSerializer):
    deposit = serializers.SerializerMethodField()

    class Meta:
        model = DepositOption
        fields = '__all__'

    def get_deposit(self, obj):
        # obj는 DepositOption 인스턴스입니다.
        deposit = obj.deposit  # DepositOption에 연결된 Deposit 인스턴스
        
        if deposit and deposit.bank == self.context.get('bank'):
            return DepositSerializer(deposit).data
        return None

class DepositOptionCompound1Serializer(serializers.ModelSerializer):
    deposit = DepositSerializer()
    effective_rate = serializers.SerializerMethodField()
    class Meta:
        model = DepositOption
        fields = ['id', 'deposit', 'effective_rate']
    # 1년 기준 연 복리 예금 수익률 : 총기간수익률 / 연수
    def get_effective_rate(self, obj):
        return round(((1 + obj.intr_rate / 100) ** (obj.period / 12) - 1)* 100 / (obj.period / 12),3)

class DepositOptionCompound2Serializer(serializers.ModelSerializer):
    deposit = DepositSerializer()
    effective_rate = serializers.SerializerMethodField()
    class Meta:
        model = DepositOption
        fields = '__all__'
    # 원금 / n빵 * 12/ 연이자율 * ((1+연이자율/12) ** (n+1)-1) - 1
    def get_effective_rate(self, obj):
        return round(obj.intr_rate * (obj.period + 1) / 24,3)
        
class DepositListSerializer(serializers.ModelSerializer):
    standard = serializers.SerializerMethodField()
    depositoption_set = DepositOptionsSerializer(many=True, read_only=True)
    class Meta:
        model = Deposit
        fields = '__all__'

    def get_standard(self, obj):
        # 연결된 DepositOption 중 intr_rate가 가장 작은 것을 기준으로 정렬
        min_intr_rate_option = obj.get_min_intr_rate_option()
        if min_intr_rate_option:
            return DepositOptionsSerializer(min_intr_rate_option).data
        return None
