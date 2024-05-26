from django.db import models
from django.conf import settings

# Create your models here.
class Deposit(models.Model):
    product_code = models.TextField(blank=True,null=True) # 상품코드
    bank_code =models.TextField(blank=True,null=True) # 금융회사 코드
    bank = models.TextField(blank=True,null=True) # 은행명
    etc_note = models.TextField(blank=True,null=True) # 가입조건
    product = models.TextField(blank=True,null=True) # 상품명
    max_limit = models.IntegerField(blank=True,null=True) # 가입한도
    start = models.TextField(blank=True,null=True) # 공시일자
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='like_deposits') # 유저가 관심있는 예적금
    mtrt_int = models.TextField(blank=True,null=True) # 만기 후 이자율
    spcl_cnd = models.TextField(blank=True,null=True) # 우대조건
    join_member = models.TextField(blank=True,null=True) # 가입대상
    
    def get_min_intr_rate_option(self):
        return self.depositoption_set.order_by('intr_rate').first()

class DepositOption(models.Model):
    period = models.IntegerField() # 예적금 기간
    intr_type = models.CharField(max_length=5) # 단(S)/복리(M)
    intr_rate = models.FloatField() # 기본금리
    intr_rate2 = models.FloatField() # 최고금리
    rsrv_type_nm = models.TextField(blank=True,null=True) # 자유적립식 / 정액적립식
    deposit = models.ForeignKey(Deposit,on_delete=models.CASCADE,null=True) # 해당 상품의 각 조건들     