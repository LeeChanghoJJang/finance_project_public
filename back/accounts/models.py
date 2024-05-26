from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    like_bank = models.CharField(max_length=100) # 유저가 선호하는 은행
    pass
